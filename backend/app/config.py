from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = Field(default='Coloring Book API', alias='APP_NAME')
    base_url: str = Field(default='http://10.0.2.2:8000', alias='BASE_URL')
    upload_dir: str = Field(default='data/uploads', alias='UPLOAD_DIR')
    output_dir: str = Field(default='data/outputs', alias='OUTPUT_DIR')
    pdf_dir: str = Field(default='data/pdfs', alias='PDF_DIR')
    device: str = Field(default='cpu', alias='DEVICE')
    enable_ai: bool = Field(default=True, alias='ENABLE_AI')
    hf_model_id: str = Field(default='runwayml/stable-diffusion-v1-5', alias='HF_MODEL_ID')
    max_image_size: int = Field(default=1600, alias='MAX_IMAGE_SIZE')
    cors_origins: str = Field(default='*', alias='CORS_ORIGINS')

    @property
    def cors_origin_list(self) -> List[str]:
        if self.cors_origins.strip() == '*':
            return ['*']
        return [item.strip() for item in self.cors_origins.split(',') if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
