from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

from app.config import get_settings


settings = get_settings()


def normalize_and_limit(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert('RGB')
    max_size = settings.max_image_size
    image.thumbnail((max_size, max_size))
    return image


def save_pil_image(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format='PNG')


def read_image_from_bytes(raw: bytes) -> Image.Image:
    return Image.open(BytesIO(raw))
