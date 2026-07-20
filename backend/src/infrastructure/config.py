"""애플리케이션 설정"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/celebrity_booking"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@celebrity-booking.com"
    SMTP_USE_TLS: bool = True
    # 견적 등록 알림 수신 관리자 메일 (쉼표 구분)
    ADMIN_NOTIFICATION_EMAILS: str = "brassonitent1016@gmail.com"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]
    # 견적 첨부파일 허용 확장자 (문서/이미지/압축)
    ALLOWED_ATTACHMENT_EXTS: list[str] = [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".hwp", ".hwpx", ".txt", ".zip",
        ".jpg", ".jpeg", ".png", ".webp",
    ]

    # Oracle Object Storage (S3 호환 API) — 미설정 시 로컬 uploads/ 폴백
    OCI_NAMESPACE: str = ""
    OCI_BUCKET_NAME: str = ""
    OCI_REGION: str = ""
    OCI_ACCESS_KEY: str = ""
    OCI_SECRET_KEY: str = ""

    # App
    APP_NAME: str = "연예인 섭외대행 시스템"
    DEBUG: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
