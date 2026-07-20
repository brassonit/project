"""초기 데이터 시딩 스크립트 — 카테고리/장르/관리자
(테이블 생성과 기본 시드는 scripts/create_tables.sql 참조)
"""

from src.infrastructure.database.connection import SessionLocal
from src.infrastructure.database.models import CategoryModel, GenreModel, UserModel
from src.infrastructure.security.password_hasher import PasswordHasher

CATEGORIES: dict[str, list[str]] = {
    "대중가수": ["아이돌", "발라드", "트로트", "힙합"],
    "음악": ["재즈", "클래식", "뮤지컬", "국악"],
    "강연": ["셀럽", "배우"],
    "사회자": ["전문MC", "아나운서"],
    "퍼포먼스": ["마술", "무용", "댄스"],
}


def seed_categories(db) -> None:
    """GNB 카테고리 + 하위 장르"""
    if db.query(CategoryModel).count() > 0:
        print("카테고리 데이터가 이미 존재합니다.")
        return
    for ci, (cat_name, genres) in enumerate(CATEGORIES.items(), start=1):
        cat = CategoryModel(name=cat_name, sort_order=ci)
        db.add(cat)
        db.flush()
        for gi, genre_name in enumerate(genres, start=1):
            db.add(GenreModel(category_id=cat.id, name=genre_name, sort_order=gi))
    db.commit()
    print(f"카테고리 {len(CATEGORIES)}개 + 장르 시드 완료")


def seed_admin(db) -> None:
    """기본 관리자 계정 생성"""
    existing = db.query(UserModel).filter(UserModel.email == "admin@brassonit.com").first()
    if existing:
        print("관리자 계정이 이미 존재합니다.")
        return

    hasher = PasswordHasher()
    admin = UserModel(
        email="admin@brassonit.com",
        hashed_password=hasher.hash("Admin1234!"),
        role="admin",
        is_verified=True,
    )
    db.add(admin)
    db.commit()
    print("관리자 계정 생성 완료: admin@brassonit.com / Admin1234!")


def run_seed() -> None:
    """시드 데이터 실행"""
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_admin(db)
        print("시드 데이터 생성 완료!")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
