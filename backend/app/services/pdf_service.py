from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class PdfService:
    def save_a4_pdf(self, image_path: Path, pdf_path: Path) -> None:
        page = canvas.Canvas(str(pdf_path), pagesize=A4)
        page_w, page_h = A4
        margin = 36

        img = Image.open(image_path)
        iw, ih = img.size

        ratio = min((page_w - 2 * margin) / iw, (page_h - 2 * margin) / ih)
        draw_w = iw * ratio
        draw_h = ih * ratio

        x = (page_w - draw_w) / 2
        y = (page_h - draw_h) / 2

        page.drawImage(ImageReader(img), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True)
        page.showPage()
        page.save()
