"""Category / Genre 도메인 엔티티 — GNB 카테고리와 하위 장르"""

from dataclasses import dataclass, field


@dataclass
class Genre:
    id: int
    category_id: int
    name: str
    sort_order: int = 0


@dataclass
class Category:
    id: int
    name: str
    sort_order: int = 0
    genres: list[Genre] = field(default_factory=list)
