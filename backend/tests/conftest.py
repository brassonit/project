"""테스트 공통 설정"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.infrastructure.database.connection import Base, get_db
from src.infrastructure.database.models import (  # noqa: F401
    ArtistModel,
    InquiryModel,
    PerformanceModel,
    UserModel,
)
from src.main import app

# SQLite 인메모리 테스트 DB
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    """각 테스트 전에 DB 테이블 생성, 후에 삭제"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_db):
    """API 와 테스트 코드가 동일한 세션 공유"""
    session = TestingSessionLocal()

    def _get_test_db():
        yield session

    app.dependency_overrides[get_db] = _get_test_db
    try:
        yield session
    finally:
        session.close()
        app.dependency_overrides.clear()
