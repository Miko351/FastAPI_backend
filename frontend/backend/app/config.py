from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"

class BaseConfig(BaseSettings):
    DB_URL: Optional[str] = None
    DB_NAME: Optional[str] = None
    CLOUDINARY_SECRET_KEY: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_CLOUD_NAME: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),      # ✅ 절대경로 적용
        env_file_encoding="utf-8",
        extra="ignore",
    )

def require_settings(s: "BaseConfig") -> "BaseConfig":
    missing = [k for k in ("DB_URL", "DB_NAME") if not getattr(s, k)]
    if missing:
        raise RuntimeError(f".env 로드 실패 → {', '.join(missing)} 비었음. 경로 확인 필요: {ENV_PATH}")
    return s

settings = require_settings(BaseConfig())  # ✅ 필수값 검증