from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import get_settings
from app.schemas import GenerateResponse, HealthResponse
from app.services.face_service import FaceService
from app.services.generation_service import GenerationService
from app.services.lineart_service import LineArtService
from app.services.pdf_service import PdfService
from app.storage.file_store import ensure_dirs, new_job_id, output_path, pdf_path, upload_path
from app.utils.image_utils import normalize_and_limit, read_image_from_bytes, save_pil_image

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

ensure_dirs()
face_service = FaceService()
generation_service = GenerationService()
lineart_service = LineArtService()
pdf_service = PdfService()


@app.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status='ok',
        ai_enabled=settings.enable_ai,
        ai_loaded=generation_service.ai_loaded,
        device=settings.device,
    )


@app.post('/generate', response_model=GenerateResponse)
async def generate(file: UploadFile = File(...)) -> GenerateResponse:
    suffix = Path(file.filename or 'upload.jpg').suffix.lower() or '.jpg'
    if suffix not in {'.jpg', '.jpeg', '.png', '.webp'}:
        raise HTTPException(status_code=400, detail='Obsługiwane pliki: jpg, jpeg, png, webp.')

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail='Plik jest pusty.')

    try:
        image = read_image_from_bytes(raw)
    except Exception:
        raise HTTPException(status_code=400, detail='Nie udało się odczytać obrazu.')

    image = normalize_and_limit(image)

    job_id = new_job_id()
    input_file = upload_path(job_id, suffix)
    image.save(input_file)

    face_result = face_service.extract_face_region(image)
    if face_result is None:
        raise HTTPException(status_code=400, detail='Nie wykryto twarzy na zdjęciu.')

    dwarf_image, used_ai = generation_service.generate_dwarf(face_result.image)
    coloring_page = lineart_service.to_coloring_page(dwarf_image)

    result_image_path = output_path(job_id)
    result_pdf_path = pdf_path(job_id)

    save_pil_image(coloring_page, result_image_path)
    pdf_service.save_a4_pdf(result_image_path, result_pdf_path)

    return GenerateResponse(
        job_id=job_id,
        preview_url=f'{settings.base_url}/result/{job_id}.png',
        pdf_url=f'{settings.base_url}/result/{job_id}.pdf',
        used_ai=used_ai,
    )


@app.get('/result/{filename}')
def get_result(filename: str):
    if filename.endswith('.png'):
        path = Path(settings.output_dir) / filename
        media_type = 'image/png'
    elif filename.endswith('.pdf'):
        path = Path(settings.pdf_dir) / filename
        media_type = 'application/pdf'
    else:
        raise HTTPException(status_code=404, detail='Nieobsługiwany typ pliku.')

    if not path.exists():
        raise HTTPException(status_code=404, detail='Plik nie istnieje.')

    return FileResponse(path=str(path), media_type=media_type, filename=path.name)
