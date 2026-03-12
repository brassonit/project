"""Performance 엔티티 유닛 테스트 (RED Phase)"""

from datetime import date, datetime
from uuid import uuid4

import pytest
from src.domain.entities.performance import Performance


class TestPerformanceEntity:
    def test_create_performance_with_valid_data(self):
        perf = Performance(
            id=uuid4(),
            title="2026 신년 콘서트",
            description="새해를 맞이하는 특별 콘서트",
            event_date=date(2026, 3, 15),
            venue="세종문화회관",
            image_url="concert.jpg",
            artist_id=uuid4(),
            is_featured=True,
            created_at=datetime.now(),
        )
        assert perf.title == "2026 신년 콘서트"
        assert perf.venue == "세종문화회관"
        assert perf.is_featured is True

    def test_performance_without_artist(self):
        perf = Performance(
            id=uuid4(),
            title="오케스트라 공연",
            description="클래식 오케스트라 공연",
            event_date=date(2026, 6, 1),
            venue="예술의전당",
            image_url=None,
            artist_id=None,
            is_featured=False,
            created_at=datetime.now(),
        )
        assert perf.artist_id is None
        assert perf.image_url is None

    def test_performance_title_required(self):
        with pytest.raises(ValueError, match="제목"):
            Performance(
                id=uuid4(),
                title="",
                description="설명",
                event_date=date(2026, 6, 1),
                venue="장소",
                image_url=None,
                artist_id=None,
                is_featured=False,
                created_at=datetime.now(),
            )

    def test_performance_venue_required(self):
        with pytest.raises(ValueError, match="장소"):
            Performance(
                id=uuid4(),
                title="공연 제목",
                description="설명",
                event_date=date(2026, 6, 1),
                venue="",
                image_url=None,
                artist_id=None,
                is_featured=False,
                created_at=datetime.now(),
            )

    def test_performance_toggle_featured(self):
        perf = Performance(
            id=uuid4(),
            title="공연",
            description="설명",
            event_date=date(2026, 6, 1),
            venue="장소",
            image_url=None,
            artist_id=None,
            is_featured=False,
            created_at=datetime.now(),
        )
        perf.set_featured(True)
        assert perf.is_featured is True
        perf.set_featured(False)
        assert perf.is_featured is False
