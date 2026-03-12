"""인증 Use Case 유닛 테스트 (RED Phase)"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from src.application.use_cases.auth.login_user import LoginUser
from src.application.use_cases.auth.register_user import RegisterUser
from src.application.use_cases.auth.verify_email import VerifyEmail
from src.domain.entities.user import User, UserRole

# === Fixtures ===


@pytest.fixture
def mock_user_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def mock_password_hasher():
    hasher = MagicMock()
    hasher.hash.return_value = "hashed_password_123"
    hasher.verify.return_value = True
    return hasher


@pytest.fixture
def mock_jwt_handler():
    handler = MagicMock()
    handler.create_access_token.return_value = "access_token_abc"
    handler.create_refresh_token.return_value = "refresh_token_xyz"
    return handler


@pytest.fixture
def mock_email_service():
    service = AsyncMock()
    return service


@pytest.fixture
def register_use_case(mock_user_repo, mock_password_hasher, mock_email_service):
    return RegisterUser(
        user_repo=mock_user_repo,
        password_hasher=mock_password_hasher,
        email_service=mock_email_service,
    )


@pytest.fixture
def login_use_case(mock_user_repo, mock_password_hasher, mock_jwt_handler):
    return LoginUser(
        user_repo=mock_user_repo,
        password_hasher=mock_password_hasher,
        jwt_handler=mock_jwt_handler,
    )


@pytest.fixture
def verify_use_case(mock_user_repo):
    return VerifyEmail(user_repo=mock_user_repo)


@pytest.fixture
def verified_user():
    return User(
        id=uuid4(),
        email="verified@example.com",
        hashed_password="hashed_pw",
        role=UserRole.CUSTOMER,
        is_verified=True,
        verification_token=None,
        created_at=datetime.now(),
    )


@pytest.fixture
def unverified_user():
    return User(
        id=uuid4(),
        email="unverified@example.com",
        hashed_password="hashed_pw",
        role=UserRole.CUSTOMER,
        is_verified=False,
        verification_token="token_abc123",
        created_at=datetime.now(),
    )


# === RegisterUser Tests ===


class TestRegisterUser:
    @pytest.mark.asyncio
    async def test_register_with_valid_data(self, register_use_case, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None
        mock_user_repo.save.return_value = User(
            id=uuid4(),
            email="new@example.com",
            hashed_password="hashed_password_123",
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token="some_token",
            created_at=datetime.now(),
        )

        result = await register_use_case.execute(
            email="new@example.com",
            password="SecurePass123!",
        )

        assert result.email == "new@example.com"
        assert result.is_verified is False
        mock_user_repo.save.assert_called_once()
        mock_user_repo.find_by_email.assert_called_once_with("new@example.com")

    @pytest.mark.asyncio
    async def test_register_sends_verification_email(self, register_use_case, mock_user_repo, mock_email_service):
        mock_user_repo.find_by_email.return_value = None
        mock_user_repo.save.return_value = User(
            id=uuid4(),
            email="new@example.com",
            hashed_password="hashed_password_123",
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token="some_token",
            created_at=datetime.now(),
        )

        await register_use_case.execute(email="new@example.com", password="SecurePass123!")

        mock_email_service.send_verification_email.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises(self, register_use_case, mock_user_repo, verified_user):
        mock_user_repo.find_by_email.return_value = verified_user

        with pytest.raises(ValueError, match="이미 등록된 이메일"):
            await register_use_case.execute(email="verified@example.com", password="SecurePass123!")

    @pytest.mark.asyncio
    async def test_register_weak_password_raises(self, register_use_case, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="비밀번호"):
            await register_use_case.execute(email="new@example.com", password="123")

    @pytest.mark.asyncio
    async def test_register_invalid_email_raises(self, register_use_case, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="이메일"):
            await register_use_case.execute(email="invalid-email", password="SecurePass123!")

    @pytest.mark.asyncio
    async def test_register_hashes_password(self, register_use_case, mock_user_repo, mock_password_hasher):
        mock_user_repo.find_by_email.return_value = None
        mock_user_repo.save.return_value = User(
            id=uuid4(),
            email="new@example.com",
            hashed_password="hashed_password_123",
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token="token",
            created_at=datetime.now(),
        )

        await register_use_case.execute(email="new@example.com", password="SecurePass123!")

        mock_password_hasher.hash.assert_called_once_with("SecurePass123!")


# === VerifyEmail Tests ===


class TestVerifyEmail:
    @pytest.mark.asyncio
    async def test_verify_valid_token(self, verify_use_case, mock_user_repo, unverified_user):
        mock_user_repo.find_by_verification_token.return_value = unverified_user

        result = await verify_use_case.execute(token="token_abc123")

        assert result.is_verified is True
        assert result.verification_token is None
        mock_user_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_verify_invalid_token_raises(self, verify_use_case, mock_user_repo):
        mock_user_repo.find_by_verification_token.return_value = None

        with pytest.raises(ValueError, match="유효하지 않은 인증 토큰"):
            await verify_use_case.execute(token="bad_token")

    @pytest.mark.asyncio
    async def test_verify_already_verified_raises(self, verify_use_case, mock_user_repo, verified_user):
        verified_user.verification_token = "leftover_token"
        mock_user_repo.find_by_verification_token.return_value = verified_user

        with pytest.raises(ValueError, match="이미 인증된"):
            await verify_use_case.execute(token="leftover_token")


# === LoginUser Tests ===


class TestLoginUser:
    @pytest.mark.asyncio
    async def test_login_verified_user_success(self, login_use_case, mock_user_repo, mock_jwt_handler, verified_user):
        mock_user_repo.find_by_email.return_value = verified_user

        result = await login_use_case.execute(email="verified@example.com", password="correct_password")

        assert result["access_token"] == "access_token_abc"
        assert result["token_type"] == "bearer"
        mock_jwt_handler.create_access_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_unverified_user_raises(self, login_use_case, mock_user_repo, unverified_user):
        mock_user_repo.find_by_email.return_value = unverified_user

        with pytest.raises(ValueError, match="이메일 인증"):
            await login_use_case.execute(email="unverified@example.com", password="password")

    @pytest.mark.asyncio
    async def test_login_wrong_password_raises(
        self, login_use_case, mock_user_repo, mock_password_hasher, verified_user
    ):
        mock_user_repo.find_by_email.return_value = verified_user
        mock_password_hasher.verify.return_value = False

        with pytest.raises(ValueError, match="비밀번호가 일치하지 않습니다"):
            await login_use_case.execute(email="verified@example.com", password="wrong_password")

    @pytest.mark.asyncio
    async def test_login_nonexistent_email_raises(self, login_use_case, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="등록되지 않은 이메일"):
            await login_use_case.execute(email="noone@example.com", password="password")

    @pytest.mark.asyncio
    async def test_login_returns_user_info(self, login_use_case, mock_user_repo, verified_user):
        mock_user_repo.find_by_email.return_value = verified_user

        result = await login_use_case.execute(email="verified@example.com", password="correct")

        assert "user" in result
        assert result["user"].email == "verified@example.com"
