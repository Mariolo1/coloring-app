from __future__ import annotations

import logging
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GenerationService:
    def __init__(self) -> None:
        self.pipe = None
        self.ai_loaded = False
        if settings.enable_ai:
            self._try_load_pipeline()

    def _try_load_pipeline(self) -> None:
        try:
            import torch
            from diffusers import StableDiffusionImg2ImgPipeline

            dtype = torch.float16 if settings.device == 'cuda' else torch.float32
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                settings.hf_model_id,
                torch_dtype=dtype,
                safety_checker=None,
            )
            self.pipe = self.pipe.to(settings.device)
            self.ai_loaded = True
            logger.info('Loaded diffusion pipeline: %s', settings.hf_model_id)
        except Exception as exc:  # pragma: no cover
            self.ai_loaded = False
            self.pipe = None
            logger.warning('Could not load diffusion pipeline, using fallback mode. Reason: %s', exc)

    def _prepare_canvas(self, face_crop: Image.Image) -> Image.Image:
        canvas = Image.new('RGB', (768, 768), 'white')
        resized_face = ImageOps.contain(face_crop.convert('RGB'), (260, 260))
        face_x = (768 - resized_face.width) // 2
        face_y = 165
        canvas.paste(resized_face, (face_x, face_y))

        draw = ImageDraw.Draw(canvas)
        draw.polygon([(384, 40), (250, 220), (518, 220)], outline='black', width=5)
        draw.ellipse((220, 120, 548, 450), outline='black', width=4)
        draw.arc((180, 260, 588, 620), start=15, end=165, fill='black', width=6)
        draw.rectangle((275, 420, 493, 700), outline='black', width=4)
        draw.line((275, 500, 215, 665), fill='black', width=5)
        draw.line((493, 500, 553, 665), fill='black', width=5)
        draw.line((320, 700, 270, 760), fill='black', width=5)
        draw.line((448, 700, 498, 760), fill='black', width=5)
        return canvas

    def _fallback_generate(self, face_crop: Image.Image) -> Image.Image:
        base = self._prepare_canvas(face_crop)
        softened = base.filter(ImageFilter.SMOOTH_MORE)
        softened = ImageOps.autocontrast(softened)
        return softened

    def generate_dwarf(self, face_crop: Image.Image) -> tuple[Image.Image, bool]:
        init_image = self._prepare_canvas(face_crop)

        if not self.ai_loaded or self.pipe is None:
            return self._fallback_generate(face_crop), False

        prompt = (
            'cute fantasy dwarf, coloring book character, simple costume, front view, '
            'large beard, dwarf hat, centered portrait, preserve face likeness, '
            'child friendly illustration, clean outlines, minimal background'
        )
        negative_prompt = (
            'photo realism, dark scene, extra limbs, extra face, deformed eyes, '
            'ugly hands, text, watermark, detailed background, shadows, grey fill'
        )

        try:
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=init_image,
                strength=0.45,
                guidance_scale=7.5,
                num_inference_steps=30,
            ).images[0]
            return result, True
        except Exception as exc:  # pragma: no cover
            logger.warning('Generation failed, switching to fallback mode. Reason: %s', exc)
            return self._fallback_generate(face_crop), False
