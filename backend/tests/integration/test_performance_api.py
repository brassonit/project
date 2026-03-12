"""공연 API 엔드포인트 통합 테스트"""

import uuid
from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient
from src.infrastructure.database.models import PerformanceModel
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


SAMPLE_PERFORMANCE = {
    "title": "봄 콘서트",
    "description": "봄맞이 특별 콘서트",
    "event_date": "2026-04-15",
    "venue": "예술의전당",
    "is_featured": False,
}


@pytest.fixture
def seed_performances(db_session):
    performances = [
        PerformanceModel(
            id=uuid.uuid4(),
            title="봄 콘서트",
            description="봄맞이",
            event_date=date(2026, 4, 15),
            venue="예술의전당",
            is_featured=True,
        ),
        PerformanceModel(
            id=uuid.uuid4(),
            title="여름 페스티벌",
            description="여름 축제",
            event_date=date(2026, 7, 20),
            venue="올림픽공원",
            is_featured=False,
        ),
        PerformanceModel(
            id=uuid.uuid4(),
            title="가을 리사이틀",
            description="가을 공연",
            event_date=date(2026, 10, 5),
            venue="세종문화회관",
            is_featured=True,
        ),
    ]
    for p in performances:
        db_session.add(p)
    db_session.commit()
    return performances


class TestListPerformancesAPI:
    @pytest.mark.asyncio
    async def test_list_all(self, client, seed_performances):
        response = await client.get("/api/performances")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["performances"]) == 3

    @pytest.mark.asyncio
    async def test_list_featured(self, client, seed_performances):
        response = await client.get("/api/performances/featured")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert all(p["is_featured"] for p in data["performances"])

    @pytest.mark.asyncio
    async def test_list_featured_query_param(self, client, seed_performances):
        response = await client.get("/api/performances?featured=true")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2

    @pytest.mark.asyncio
    async def test_list_pagination(self, client, seed_performances):
        response = await client.get("/api/performances?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["performances"]) == 2
        assert data["total"] == 3


class TestGetPerformanceAPI:
    @pytest.mark.asyncio
    async def test_get_detail(self, client, seed_performances):
        pid = str(seed_performances[0].id)
        response = await client.get(f"/api/performances/{pid}")
        assert response.status_code == 200
        assert response.json()["title"] == "봄 콘서트"

    @pytest.mark.asyncio
    async def test_get_not_found(self, client):
        response = await client.get(f"/api/performances/{uuid.uuid4()}")
        assert response.status_code == 404


class TestCreatePerformanceAPI:
    @pytest.mark.asyncio
    async def test_create_admin(self, client, admin_token):
        response = await client.post(
            "/api/performances",
            json=SAMPLE_PERFORMANCE,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "봄 콘서트"
        assert data["venue"] == "예술의전당"

    @pytest.mark.asyncio
    async def test_create_customer_forbidden(self, client, user_token):
        response = await client.post(
            "/api/performances",
            json=SAMPLE_PERFORMANCE,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_no_auth(self, client):
        response = await client.post("/api/performances", json=SAMPLE_PERFORMANCE)
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_create_empty_title(self, client, admin_token):
        data = {**SAMPLE_PERFORMANCE, "title": ""}
        response = await client.post(
            "/api/performances",
            json=data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400


class TestUpdatePerformanceAPI:
    @pytest.mark.asyncio
    async def test_update_admin(self, client, admin_token, seed_performances):
        pid = str(seed_performances[0].id)
        response = await client.put(
            f"/api/performances/{pid}",
            json={"title": "수정된 콘서트"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "수정된 콘서트"

    @pytest.mark.asyncio
    async def test_toggle_featured(self, client, admin_token, seed_performances):
        pid = str(seed_performances[0].id)
        response = await client.put(
            f"/api/performances/{pid}",
            json={"is_featured": False},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["is_featured"] is False

    @pytest.mark.asyncio
    async def test_update_customer_forbidden(self, client, user_token, seed_performances):
        pid = str(seed_performances[0].id)
        response = await client.put(
            f"/api/performances/{pid}",
            json={"title": "해킹"},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_not_found(self, client, admin_token):
        response = await client.put(
            f"/api/performances/{uuid.uuid4()}",
            json={"title": "없음"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404


class TestDeletePerformanceAPI:
    @pytest.mark.asyncio
    async def test_delete_admin(self, client, admin_token, seed_performances):
        pid = str(seed_performances[0].id)
        response = await client.delete(
            f"/api/performances/{pid}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

        get_resp = await client.get(f"/api/performances/{pid}")
        assert get_resp.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_customer_forbidden(self, client, user_token, seed_performances):
        pid = str(seed_performances[0].id)
        response = await client.delete(
            f"/api/performances/{pid}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_not_found(self, client, admin_token):
        response = await client.delete(
            f"/api/performances/{uuid.uuid4()}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
