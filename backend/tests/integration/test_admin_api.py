"""관리자 API 엔드포인트 통합 테스트"""

import io
import uuid
from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient
from src.infrastructure.database.models import (
    ArtistModel,
    InquiryModel,
    PerformanceModel,
)
from src.infrastructure.security.jwt_handler import JWTHandler
from src.main import app


@pytest.fixture
async def client(db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def admin_token(db_session):
    handler = JWTHandler()
    return handler.create_access_token(user_id=uuid.uuid4(), role="admin")


@pytest.fixture
def user_token(db_session):
    handler = JWTHandler()
    return handler.create_access_token(user_id=uuid.uuid4(), role="customer")


@pytest.fixture
def seed_data(db_session):
    """대시보드 테스트용 시드 데이터"""
    artists = [
        ArtistModel(
            id=uuid.uuid4(),
            name="활성 가수",
            category="singer",
            description="설명",
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="활성 댄서",
            category="dancer",
            description="설명",
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="비활성 뮤지션",
            category="musician",
            description="설명",
            is_active=False,
        ),
    ]
    performances = [
        PerformanceModel(
            id=uuid.uuid4(),
            title="공연1",
            description="설명",
            event_date=date(2026, 4, 15),
            venue="장소",
            is_featured=True,
        ),
        PerformanceModel(
            id=uuid.uuid4(),
            title="공연2",
            description="설명",
            event_date=date(2026, 7, 20),
            venue="장소",
            is_featured=False,
        ),
    ]
    inquiries = [
        InquiryModel(
            id=uuid.uuid4(),
            name="홍길동",
            email="hong@example.com",
            subject="문의1",
            message="내용",
            status="pending",
        ),
        InquiryModel(
            id=uuid.uuid4(),
            name="김철수",
            email="kim@example.com",
            subject="문의2",
            message="내용",
            status="replied",
            admin_reply="답변",
        ),
        InquiryModel(
            id=uuid.uuid4(),
            name="이영희",
            email="lee@example.com",
            subject="문의3",
            message="내용",
            status="closed",
        ),
    ]
    for item in artists + performances + inquiries:
        db_session.add(item)
    db_session.commit()
    return {"artists": artists, "performances": performances, "inquiries": inquiries}


# === 대시보드 ===


class TestDashboardAPI:
    @pytest.mark.asyncio
    async def test_dashboard_admin(self, client, admin_token, seed_data):
        response = await client.get(
            "/api/admin/dashboard",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()

        assert data["artists"]["total"] == 3
        assert data["artists"]["active"] == 2
        assert data["artists"]["inactive"] == 1
        assert data["performances"]["total"] == 2
        assert data["performances"]["featured"] == 1
        assert data["inquiries"]["total"] == 3
        assert data["inquiries"]["pending"] == 1
        assert data["inquiries"]["replied"] == 1
        assert data["inquiries"]["closed"] == 1

    @pytest.mark.asyncio
    async def test_dashboard_customer_forbidden(self, client, user_token):
        response = await client.get(
            "/api/admin/dashboard",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_dashboard_no_auth(self, client):
        response = await client.get("/api/admin/dashboard")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_dashboard_empty_db(self, client, admin_token):
        response = await client.get(
            "/api/admin/dashboard",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["artists"]["total"] == 0
        assert data["performances"]["total"] == 0
        assert data["inquiries"]["total"] == 0


# === 관리자 아티스트 목록 (비활성 포함) ===


class TestAdminArtistsAPI:
    @pytest.mark.asyncio
    async def test_admin_artists_includes_inactive(self, client, admin_token, seed_data):
        response = await client.get(
            "/api/admin/artists",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        # 비활성 포함하여 3명 모두 반환
        assert data["total"] == 3
        assert len(data["artists"]) == 3

    @pytest.mark.asyncio
    async def test_admin_artists_vs_public(self, client, admin_token, seed_data):
        # 공개 API: 활성만
        public_resp = await client.get("/api/artists")
        assert public_resp.json()["total"] == 2

        # 관리자 API: 비활성 포함
        admin_resp = await client.get(
            "/api/admin/artists",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert admin_resp.json()["total"] == 3

    @pytest.mark.asyncio
    async def test_admin_artists_customer_forbidden(self, client, user_token):
        response = await client.get(
            "/api/admin/artists",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_artists_pagination(self, client, admin_token, seed_data):
        response = await client.get(
            "/api/admin/artists?skip=0&limit=2",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) == 2
        assert data["total"] == 3


# === 이미지 업로드 ===


class TestImageUploadAPI:
    @pytest.mark.asyncio
    async def test_upload_image_admin(self, client, admin_token, tmp_path):
        fake_image = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        response = await client.post(
            "/api/admin/upload/image",
            files={"file": ("test.png", fake_image, "image/png")},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["url"].startswith("/uploads/")
        assert data["url"].endswith(".png")

    @pytest.mark.asyncio
    async def test_upload_image_customer_forbidden(self, client, user_token):
        fake_image = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        response = await client.post(
            "/api/admin/upload/image",
            files={"file": ("test.png", fake_image, "image/png")},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_upload_invalid_type(self, client, admin_token):
        fake_file = io.BytesIO(b"not an image")
        response = await client.post(
            "/api/admin/upload/image",
            files={"file": ("test.txt", fake_file, "text/plain")},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400
