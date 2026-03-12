"""초기 데이터 시딩 스크립트"""

import uuid
from datetime import date

from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.database.models import (
    ArtistModel,
    PerformanceModel,
    UserModel,
)
from src.infrastructure.security.password_hasher import PasswordHasher


def seed_admin(db) -> None:
    """기본 관리자 계정 생성"""
    existing = db.query(UserModel).filter(UserModel.email == "admin@brassonit.com").first()
    if existing:
        print("관리자 계정이 이미 존재합니다.")
        return

    hasher = PasswordHasher()
    admin = UserModel(
        id=uuid.uuid4(),
        email="admin@brassonit.com",
        hashed_password=hasher.hash("Admin1234!"),
        role="admin",
        is_verified=True,
    )
    db.add(admin)
    db.commit()
    print("관리자 계정 생성 완료: admin@brassonit.com / Admin1234!")


def seed_sample_artists(db) -> None:
    """샘플 아티스트 데이터"""
    if db.query(ArtistModel).count() > 0:
        print("아티스트 데이터가 이미 존재합니다.")
        return

    artists = [
        ArtistModel(
            id=uuid.uuid4(),
            name="김나래",
            category="singer",
            description="다양한 장르를 소화하는 인기 가수입니다.",
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="박지민",
            category="dancer",
            description="현대무용과 스트릿 댄스를 전문으로 하는 댄서입니다.",
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="이서준",
            category="musician",
            description="재즈와 팝을 넘나드는 뮤지션입니다.",
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="최유진",
            category="instrumentalist",
            description="바이올린 연주자로 국내외에서 활동 중입니다.",
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="서울 챔버 오케스트라",
            category="orchestra",
            description="서울을 기반으로 활동하는 챔버 오케스트라입니다.",
            is_active=True,
        ),
    ]
    for a in artists:
        db.add(a)
    db.commit()
    print(f"샘플 아티스트 {len(artists)}명 생성 완료")


def seed_sample_performances(db) -> None:
    """샘플 공연 데이터"""
    if db.query(PerformanceModel).count() > 0:
        print("공연 데이터가 이미 존재합니다.")
        return

    performances = [
        PerformanceModel(
            id=uuid.uuid4(),
            title="봄맞이 특별 콘서트",
            description="봄을 맞이하여 다양한 아티스트가 함께하는 특별 콘서트입니다.",
            event_date=date(2026, 4, 15),
            venue="예술의전당 콘서트홀",
            is_featured=True,
        ),
        PerformanceModel(
            id=uuid.uuid4(),
            title="여름 재즈 페스티벌",
            description="여름밤을 수놓는 재즈 공연입니다.",
            event_date=date(2026, 7, 20),
            venue="올림픽공원 잔디마당",
            is_featured=True,
        ),
        PerformanceModel(
            id=uuid.uuid4(),
            title="가을 클래식 리사이틀",
            description="가을 정취와 함께하는 클래식 리사이틀입니다.",
            event_date=date(2026, 10, 5),
            venue="세종문화회관",
            is_featured=False,
        ),
    ]
    for p in performances:
        db.add(p)
    db.commit()
    print(f"샘플 공연 {len(performances)}개 생성 완료")


def run_seed() -> None:
    """시드 데이터 실행"""
    db = SessionLocal()
    try:
        seed_admin(db)
        seed_sample_artists(db)
        seed_sample_performances(db)
        print("시드 데이터 생성 완료!")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
