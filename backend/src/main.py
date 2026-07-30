"""FastAPI 애플리케이션 엔트리포인트"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.infrastructure.config import settings
from src.presentation.api.admin import router as admin_router
from src.presentation.api.artists import router as artists_router
from src.presentation.api.auth import router as auth_router
from src.presentation.api.categories import router as categories_router
from src.presentation.api.interactions import router as interactions_router
from src.presentation.api.policies import router as policies_router
from src.presentation.api.quotes import router as quotes_router
from src.presentation.api.shows import router as shows_router

app = FastAPI(
    title=settings.APP_NAME,
    description="연예인 섭외대행 · 공연기획 시스템 API",
    version="0.2.0",
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


# 업로드 파일 서빙 (프로덕션은 nginx /uploads/ alias, 로컬 개발은 여기서 직접)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(artists_router)
app.include_router(shows_router)
app.include_router(interactions_router)
app.include_router(quotes_router)
app.include_router(policies_router)
app.include_router(admin_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
