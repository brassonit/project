"""인증 API 엔드포인트 통합 테스트"""

import pytest
from httpx import ASGITransport, AsyncClient
from src.infrastructure.database.models import UserModel
from src.main import app


@pytest.fixture
async def client(db_session):
    """db_session 의존 -> 동일한 세션이 API에도 주입됨"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        response = await client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRegisterAPI:
    @pytest.mark.asyncio
    async def test_register_success(self, client):
        response = await client.post(
            "/api/auth/register",
            json={"email": "newuser@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["is_verified"] is False
        assert data["role"] == "customer"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client):
        await client.post(
            "/api/auth/register",
            json={"email": "dup@example.com", "password": "SecurePass123!"},
        )
        response = await client.post(
            "/api/auth/register",
            json={"email": "dup@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client):
        response = await client.post(
            "/api/auth/register",
            json={"email": "bad-email", "password": "SecurePass123!"},
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_register_weak_password(self, client):
        response = await client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "123"},
        )
        assert response.status_code == 400


class TestLoginAPI:
    @pytest.mark.asyncio
    async def test_login_unverified_user(self, client):
        await client.post(
            "/api/auth/register",
            json={"email": "unverified@example.com", "password": "SecurePass123!"},
        )
        response = await client.post(
            "/api/auth/login",
            json={"email": "unverified@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_login_nonexistent_email(self, client):
        response = await client.post(
            "/api/auth/login",
            json={"email": "noone@example.com", "password": "password123!"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_verified_user(self, client, db_session):
        # Register
        await client.post(
            "/api/auth/register",
            json={"email": "verified@example.com", "password": "SecurePass123!"},
        )
        # Manually verify user in DB
        user_model = db_session.query(UserModel).filter(UserModel.email == "verified@example.com").first()
        user_model.is_verified = True
        db_session.commit()

        # Login
        response = await client.post(
            "/api/auth/login",
            json={"email": "verified@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "verified@example.com"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, db_session):
        await client.post(
            "/api/auth/register",
            json={"email": "user@example.com", "password": "SecurePass123!"},
        )
        user_model = db_session.query(UserModel).filter(UserModel.email == "user@example.com").first()
        user_model.is_verified = True
        db_session.commit()

        response = await client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "WrongPass999!"},
        )
        assert response.status_code == 401


class TestVerifyEmailAPI:
    @pytest.mark.asyncio
    async def test_verify_email_success(self, client, db_session):
        await client.post(
            "/api/auth/register",
            json={"email": "toverify@example.com", "password": "SecurePass123!"},
        )
        user_model = db_session.query(UserModel).filter(UserModel.email == "toverify@example.com").first()
        token = user_model.verification_token

        response = await client.get(f"/api/auth/verify-email?token={token}")
        assert response.status_code == 200

        db_session.refresh(user_model)
        assert user_model.is_verified is True

    @pytest.mark.asyncio
    async def test_verify_email_invalid_token(self, client):
        response = await client.get("/api/auth/verify-email?token=bad_token")
        assert response.status_code == 400


class TestMeAPI:
    @pytest.mark.asyncio
    async def test_me_without_token(self, client):
        response = await client.get("/api/auth/me")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_me_with_valid_token(self, client, db_session):
        await client.post(
            "/api/auth/register",
            json={"email": "me@example.com", "password": "SecurePass123!"},
        )
        user_model = db_session.query(UserModel).filter(UserModel.email == "me@example.com").first()
        user_model.is_verified = True
        db_session.commit()

        login_response = await client.post(
            "/api/auth/login",
            json={"email": "me@example.com", "password": "SecurePass123!"},
        )
        token = login_response.json()["access_token"]

        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@example.com"
