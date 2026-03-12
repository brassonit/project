"""문의 API 엔드포인트 통합 테스트"""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from src.infrastructure.database.models import InquiryModel
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


SAMPLE_INQUIRY = {
    "name": "홍길동",
    "email": "hong@example.com",
    "phone": "010-1234-5678",
    "subject": "섭외 문의",
    "message": "가수 섭외를 요청합니다.",
}


@pytest.fixture
def seed_inquiries(db_session):
    inquiries = [
        InquiryModel(
            id=uuid.uuid4(),
            name="홍길동",
            email="hong@example.com",
            subject="문의1",
            message="내용1",
            status="pending",
        ),
        InquiryModel(
            id=uuid.uuid4(),
            name="김철수",
            email="kim@example.com",
            subject="문의2",
            message="내용2",
            status="replied",
            admin_reply="답변입니다.",
        ),
        InquiryModel(
            id=uuid.uuid4(),
            name="이영희",
            email="lee@example.com",
            subject="문의3",
            message="내용3",
            status="closed",
        ),
    ]
    for i in inquiries:
        db_session.add(i)
    db_session.commit()
    return inquiries


# === 문의 제출 (비로그인 가능) ===


class TestCreateInquiryAPI:
    @pytest.mark.asyncio
    async def test_create_without_auth(self, client):
        response = await client.post("/api/inquiries", json=SAMPLE_INQUIRY)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "홍길동"
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_create_without_phone(self, client):
        data = {k: v for k, v in SAMPLE_INQUIRY.items() if k != "phone"}
        response = await client.post("/api/inquiries", json=data)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_invalid_email(self, client):
        data = {**SAMPLE_INQUIRY, "email": "bad-email"}
        response = await client.post("/api/inquiries", json=data)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_empty_name(self, client):
        data = {**SAMPLE_INQUIRY, "name": ""}
        response = await client.post("/api/inquiries", json=data)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_empty_subject(self, client):
        data = {**SAMPLE_INQUIRY, "subject": ""}
        response = await client.post("/api/inquiries", json=data)
        assert response.status_code == 400


# === 문의 목록 (관리자 전용) ===


class TestListInquiriesAPI:
    @pytest.mark.asyncio
    async def test_list_admin(self, client, admin_token, seed_inquiries):
        response = await client.get(
            "/api/inquiries",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_list_filter_by_status(self, client, admin_token, seed_inquiries):
        response = await client.get(
            "/api/inquiries?status=pending",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["inquiries"][0]["status"] == "pending"

    @pytest.mark.asyncio
    async def test_list_customer_forbidden(self, client, user_token):
        response = await client.get(
            "/api/inquiries",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_list_no_auth(self, client):
        response = await client.get("/api/inquiries")
        assert response.status_code in (401, 403)


# === 문의 상세 (관리자 전용) ===


class TestGetInquiryAPI:
    @pytest.mark.asyncio
    async def test_get_detail(self, client, admin_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.get(
            f"/api/inquiries/{iid}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "홍길동"

    @pytest.mark.asyncio
    async def test_get_not_found(self, client, admin_token):
        response = await client.get(
            f"/api/inquiries/{uuid.uuid4()}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404


# === 문의 답변 (관리자 전용) ===


class TestReplyInquiryAPI:
    @pytest.mark.asyncio
    async def test_reply_admin(self, client, admin_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.patch(
            f"/api/inquiries/{iid}/reply",
            json={"reply": "답변 드립니다."},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "replied"
        assert data["admin_reply"] == "답변 드립니다."

    @pytest.mark.asyncio
    async def test_reply_not_found(self, client, admin_token):
        response = await client.patch(
            f"/api/inquiries/{uuid.uuid4()}/reply",
            json={"reply": "답변"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_reply_customer_forbidden(self, client, user_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.patch(
            f"/api/inquiries/{iid}/reply",
            json={"reply": "답변"},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_reply_empty_text(self, client, admin_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.patch(
            f"/api/inquiries/{iid}/reply",
            json={"reply": ""},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400


# === 문의 상태 변경 (관리자 전용) ===


class TestUpdateInquiryStatusAPI:
    @pytest.mark.asyncio
    async def test_close_inquiry(self, client, admin_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.patch(
            f"/api/inquiries/{iid}/status",
            json={"status": "closed"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "closed"

    @pytest.mark.asyncio
    async def test_invalid_status(self, client, admin_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.patch(
            f"/api/inquiries/{iid}/status",
            json={"status": "invalid"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400


# === 문의 삭제 (관리자 전용) ===


class TestDeleteInquiryAPI:
    @pytest.mark.asyncio
    async def test_delete_admin(self, client, admin_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.delete(
            f"/api/inquiries/{iid}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_customer_forbidden(self, client, user_token, seed_inquiries):
        iid = str(seed_inquiries[0].id)
        response = await client.delete(
            f"/api/inquiries/{iid}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_not_found(self, client, admin_token):
        response = await client.delete(
            f"/api/inquiries/{uuid.uuid4()}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
