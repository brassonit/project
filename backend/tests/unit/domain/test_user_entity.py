"""User 엔티티 유닛 테스트 (RED Phase)"""

from datetime import datetime
from uuid import uuid4

import pytest
from src.domain.entities.user import User, UserRole
from src.domain.value_objects.email import Email


class TestUserEntity:
    def test_create_user_with_valid_data(self):
        user = User(
            id=uuid4(),
            email="test@example.com",
            hashed_password="hashed_pw",
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token="token123",
            created_at=datetime.now(),
        )
        assert user.email == "test@example.com"
        assert user.role == UserRole.CUSTOMER
        assert user.is_verified is False
        assert user.verification_token == "token123"

    def test_user_roles(self):
        assert UserRole.CUSTOMER == "customer"
        assert UserRole.ADMIN == "admin"

    def test_user_default_not_verified(self):
        user = User(
            id=uuid4(),
            email="test@example.com",
            hashed_password="hashed_pw",
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token="token123",
            created_at=datetime.now(),
        )
        assert user.is_verified is False

    def test_user_verify_email(self):
        user = User(
            id=uuid4(),
            email="test@example.com",
            hashed_password="hashed_pw",
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token="token123",
            created_at=datetime.now(),
        )
        user.verify_email()
        assert user.is_verified is True
        assert user.verification_token is None

    def test_user_admin_role(self):
        user = User(
            id=uuid4(),
            email="admin@example.com",
            hashed_password="hashed_pw",
            role=UserRole.ADMIN,
            is_verified=True,
            verification_token=None,
            created_at=datetime.now(),
        )
        assert user.is_admin() is True

    def test_user_customer_is_not_admin(self):
        user = User(
            id=uuid4(),
            email="user@example.com",
            hashed_password="hashed_pw",
            role=UserRole.CUSTOMER,
            is_verified=True,
            verification_token=None,
            created_at=datetime.now(),
        )
        assert user.is_admin() is False


class TestEmailValueObject:
    def test_valid_email(self):
        email = Email("user@example.com")
        assert str(email) == "user@example.com"

    def test_invalid_email_no_at(self):
        with pytest.raises(ValueError, match="이메일"):
            Email("invalid-email")

    def test_invalid_email_no_domain(self):
        with pytest.raises(ValueError, match="이메일"):
            Email("user@")

    def test_invalid_email_empty(self):
        with pytest.raises(ValueError, match="이메일"):
            Email("")

    def test_email_equality(self):
        assert Email("user@example.com") == Email("user@example.com")

    def test_email_case_insensitive(self):
        assert Email("User@Example.COM") == Email("user@example.com")
