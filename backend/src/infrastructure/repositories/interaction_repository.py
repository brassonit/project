"""찜/장바구니 Repository SQLAlchemy 구현"""

from sqlalchemy.orm import Session

from src.domain.repositories.interaction_repository import IInteractionRepository
from src.infrastructure.database.models import (
    ArtistModel,
    CartModel,
    ShowModel,
    ShowWishlistModel,
    WishlistModel,
)


class SqlAlchemyInteractionRepository(IInteractionRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    async def list_wishlist(self, user_id: str) -> list[str]:
        rows = (
            self.db.query(WishlistModel)
            .filter(WishlistModel.user_id == user_id)
            .order_by(WishlistModel.created_at.desc())
            .all()
        )
        return [r.artist_id for r in rows]

    async def toggle_wishlist(self, user_id: str, artist_id: str) -> bool:
        row = (
            self.db.query(WishlistModel)
            .filter(WishlistModel.user_id == user_id, WishlistModel.artist_id == artist_id)
            .first()
        )
        if row:
            self.db.delete(row)
            self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).update(
                {ArtistModel.like_count: ArtistModel.like_count - 1}
            )
            self.db.commit()
            return False
        self.db.add(WishlistModel(user_id=user_id, artist_id=artist_id))
        self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).update(
            {ArtistModel.like_count: ArtistModel.like_count + 1}
        )
        self.db.commit()
        return True

    async def remove_wishlist(self, user_id: str, artist_ids: list[str]) -> None:
        if not artist_ids:
            return
        self.db.query(WishlistModel).filter(
            WishlistModel.user_id == user_id, WishlistModel.artist_id.in_(artist_ids)
        ).delete(synchronize_session=False)
        self.db.commit()

    async def list_show_wishlist(self, user_id: str) -> list[str]:
        rows = (
            self.db.query(ShowWishlistModel)
            .filter(ShowWishlistModel.user_id == user_id)
            .order_by(ShowWishlistModel.created_at.desc())
            .all()
        )
        return [r.show_id for r in rows]

    async def toggle_show_wishlist(self, user_id: str, show_id: str) -> bool:
        row = (
            self.db.query(ShowWishlistModel)
            .filter(ShowWishlistModel.user_id == user_id, ShowWishlistModel.show_id == show_id)
            .first()
        )
        if row:
            self.db.delete(row)
            self.db.query(ShowModel).filter(ShowModel.id == show_id).update(
                {ShowModel.like_count: ShowModel.like_count - 1}
            )
            self.db.commit()
            return False
        self.db.add(ShowWishlistModel(user_id=user_id, show_id=show_id))
        self.db.query(ShowModel).filter(ShowModel.id == show_id).update(
            {ShowModel.like_count: ShowModel.like_count + 1}
        )
        self.db.commit()
        return True

    async def remove_show_wishlist(self, user_id: str, show_ids: list[str]) -> None:
        if not show_ids:
            return
        self.db.query(ShowWishlistModel).filter(
            ShowWishlistModel.user_id == user_id, ShowWishlistModel.show_id.in_(show_ids)
        ).delete(synchronize_session=False)
        self.db.commit()

    async def list_cart(self, user_id: str) -> list[str]:
        rows = (
            self.db.query(CartModel)
            .filter(CartModel.user_id == user_id)
            .order_by(CartModel.created_at.desc())
            .all()
        )
        return [r.artist_id for r in rows]

    async def toggle_cart(self, user_id: str, artist_id: str) -> bool:
        row = (
            self.db.query(CartModel)
            .filter(CartModel.user_id == user_id, CartModel.artist_id == artist_id)
            .first()
        )
        if row:
            self.db.delete(row)
            self.db.commit()
            return False
        self.db.add(CartModel(user_id=user_id, artist_id=artist_id))
        self.db.commit()
        return True

    async def add_cart(self, user_id: str, artist_ids: list[str]) -> None:
        existing = {
            r.artist_id
            for r in self.db.query(CartModel)
            .filter(CartModel.user_id == user_id, CartModel.artist_id.in_(artist_ids))
            .all()
        }
        for aid in artist_ids:
            if aid not in existing:
                self.db.add(CartModel(user_id=user_id, artist_id=aid))
        self.db.commit()

    async def remove_cart(self, user_id: str, artist_ids: list[str]) -> None:
        if not artist_ids:
            return
        self.db.query(CartModel).filter(
            CartModel.user_id == user_id, CartModel.artist_id.in_(artist_ids)
        ).delete(synchronize_session=False)
        self.db.commit()
