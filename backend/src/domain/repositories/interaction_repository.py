"""찜(wishlist)/장바구니(cart) Repository 인터페이스"""

from abc import ABC, abstractmethod


class IInteractionRepository(ABC):
    @abstractmethod
    async def list_wishlist(self, user_id: str) -> list[str]:
        """찜한 아티스트 id 목록"""
        ...

    @abstractmethod
    async def toggle_wishlist(self, user_id: str, artist_id: str) -> bool:
        """토글 후 상태 반환 (True=찜됨). artists.like_count도 증감"""
        ...

    @abstractmethod
    async def remove_wishlist(self, user_id: str, artist_ids: list[str]) -> None: ...

    @abstractmethod
    async def list_show_wishlist(self, user_id: str) -> list[str]:
        """찜한 공연 id 목록"""
        ...

    @abstractmethod
    async def toggle_show_wishlist(self, user_id: str, show_id: str) -> bool:
        """토글 후 상태 반환 (True=찜됨). shows.like_count도 증감"""
        ...

    @abstractmethod
    async def remove_show_wishlist(self, user_id: str, show_ids: list[str]) -> None: ...

    @abstractmethod
    async def list_cart(self, user_id: str) -> list[str]:
        """장바구니 아티스트 id 목록"""
        ...

    @abstractmethod
    async def toggle_cart(self, user_id: str, artist_id: str) -> bool: ...

    @abstractmethod
    async def add_cart(self, user_id: str, artist_ids: list[str]) -> None: ...

    @abstractmethod
    async def remove_cart(self, user_id: str, artist_ids: list[str]) -> None: ...
