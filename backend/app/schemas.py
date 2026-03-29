from pydantic import BaseModel


class GenerateResponse(BaseModel):
    job_id: str
    preview_url: str
    pdf_url: str
    used_ai: bool


class HealthResponse(BaseModel):
    status: str
    ai_enabled: bool
    ai_loaded: bool
    device: str
