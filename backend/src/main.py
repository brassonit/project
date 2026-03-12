"""FastAPI 애플리케이션 엔트리포인트"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config import settings
from src.presentation.api.admin import router as admin_router
from src.presentation.api.artists import router as artists_router
from src.presentation.api.auth import router as auth_router
from src.presentation.api.inquiries import router as inquiries_router
from src.presentation.api.performances import router as performances_router

app = FastAPI(
    title=settings.APP_NAME,
    description="연예인 섭외대행 시스템 API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(artists_router)
app.include_router(performances_router)
app.include_router(inquiries_router)
app.include_router(admin_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
