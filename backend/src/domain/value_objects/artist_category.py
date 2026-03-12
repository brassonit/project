"""아티스트 카테고리 Value Object"""

from enum import Enum


class ArtistCategory(str, Enum):
    SINGER = "singer"
    DANCER = "dancer"
    MUSICIAN = "musician"
    INSTRUMENTALIST = "instrumentalist"
    ORCHESTRA = "orchestra"

    @property
    def label_ko(self) -> str:
        labels = {
            "singer": "대중가수",
            "dancer": "댄서",
            "musician": "뮤지션",
            "instrumentalist": "연주자",
            "orchestra": "오케스트라",
        }
        return labels[self.value]
