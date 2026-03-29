from pathlib import Path
from uuid import uuid4

from app.config import get_settings


settings = get_settings()


def ensure_dirs() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.output_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.pdf_dir).mkdir(parents=True, exist_ok=True)


def new_job_id() -> str:
    return str(uuid4())


def upload_path(job_id: str, ext: str = '.jpg') -> Path:
    return Path(settings.upload_dir) / f'{job_id}{ext}'


def output_path(job_id: str) -> Path:
    return Path(settings.output_dir) / f'{job_id}.png'


def pdf_path(job_id: str) -> Path:
    return Path(settings.pdf_dir) / f'{job_id}.pdf'
