"""공연 Use Case 유닛 테스트"""

from datetime import date, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from src.application.use_cases.performance.create_performance import CreatePerformance
from src.application.use_cases.performance.delete_performance import DeletePerformance
from src.application.use_cases.performance.get_performance import GetPerformance
from src.application.use_cases.performance.list_performances import ListPerformances
from src.application.use_cases.performance.update_performance import UpdatePerformance
from src.domain.entities.performance import Performance


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def sample_performance():
    return Performance(
        id=uuid4(),
        title="봄 콘서트",
        description="봄맞이 특별 콘서트",
        event_date=date(2026, 4, 15),
        venue="예술의전당",
        image_url="https://example.com/concert.jpg",
        artist_id=uuid4(),
        is_featured=True,
        created_at=datetime.now(),
    )


@pytest.fixture
def sample_performances():
    return [
        Performance(
            id=uuid4(),
            title="봄 콘서트",
            description="봄맞이 콘서트",
            event_date=date(2026, 4, 15),
            venue="예술의전당",
            image_url=None,
            artist_id=None,
            is_featured=True,
            created_at=datetime.now(),
        ),
        Performance(
            id=uuid4(),
            title="여름 페스티벌",
            description="여름 음악 축제",
            event_date=date(2026, 7, 20),
            venue="올림픽공원",
            image_url=None,
            artist_id=None,
            is_featured=False,
            created_at=datetime.now(),
        ),
        Performance(
            id=uuid4(),
            title="가을 리사이틀",
            description="가을 리사이틀",
            event_date=date(2026, 10, 5),
            venue="세종문화회관",
            image_url=None,
            artist_id=None,
            is_featured=True,
            created_at=datetime.now(),
        ),
    ]


class TestCreatePerformance:
    @pytest.mark.asyncio
    async def test_create_performance_success(self, mock_repo, sample_performance):
        mock_repo.save.return_value = sample_performance
        use_case = CreatePerformance(performance_repo=mock_repo)

        result = await use_case.execute(
            title="봄 콘서트",
            description="봄맞이 특별 콘서트",
            event_date=date(2026, 4, 15),
            venue="예술의전당",
            is_featured=True,
        )

        assert result.title == "봄 콘서트"
        assert result.is_featured is True
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_performance_empty_title_raises(self, mock_repo):
        use_case = CreatePerformance(performance_repo=mock_repo)

        with pytest.raises(ValueError, match="제목"):
            await use_case.execute(
                title="",
                description="설명",
                event_date=date(2026, 4, 15),
                venue="장소",
            )

    @pytest.mark.asyncio
    async def test_create_performance_empty_venue_raises(self, mock_repo):
        use_case = CreatePerformance(performance_repo=mock_repo)

        with pytest.raises(ValueError, match="장소"):
            await use_case.execute(
                title="제목",
                description="설명",
                event_date=date(2026, 4, 15),
                venue="",
            )


class TestGetPerformance:
    @pytest.mark.asyncio
    async def test_get_performance_success(self, mock_repo, sample_performance):
        mock_repo.find_by_id.return_value = sample_performance
        use_case = GetPerformance(performance_repo=mock_repo)

        result = await use_case.execute(performance_id=sample_performance.id)
        assert result.id == sample_performance.id

    @pytest.mark.asyncio
    async def test_get_performance_not_found(self, mock_repo):
        mock_repo.find_by_id.return_value = None
        use_case = GetPerformance(performance_repo=mock_repo)

        with pytest.raises(ValueError, match="공연을 찾을 수 없습니다"):
            await use_case.execute(performance_id=uuid4())


class TestListPerformances:
    @pytest.mark.asyncio
    async def test_list_all(self, mock_repo, sample_performances):
        mock_repo.find_all.return_value = sample_performances
        mock_repo.count_all.return_value = 3
        use_case = ListPerformances(performance_repo=mock_repo)

        result = await use_case.execute()
        assert result["total"] == 3
        assert len(result["performances"]) == 3

    @pytest.mark.asyncio
    async def test_list_featured_only(self, mock_repo, sample_performances):
        featured = [p for p in sample_performances if p.is_featured]
        mock_repo.find_featured.return_value = featured
        mock_repo.count_featured.return_value = 2
        use_case = ListPerformances(performance_repo=mock_repo)

        result = await use_case.execute(featured_only=True)
        assert result["total"] == 2
        assert all(p.is_featured for p in result["performances"])

    @pytest.mark.asyncio
    async def test_list_pagination(self, mock_repo, sample_performances):
        mock_repo.find_all.return_value = sample_performances[:2]
        mock_repo.count_all.return_value = 3
        use_case = ListPerformances(performance_repo=mock_repo)

        result = await use_case.execute(skip=0, limit=2)
        assert len(result["performances"]) == 2
        assert result["total"] == 3


class TestUpdatePerformance:
    @pytest.mark.asyncio
    async def test_update_success(self, mock_repo, sample_performance):
        mock_repo.find_by_id.return_value = sample_performance
        updated = Performance(
            id=sample_performance.id,
            title="수정된 콘서트",
            description=sample_performance.description,
            event_date=sample_performance.event_date,
            venue=sample_performance.venue,
            image_url=sample_performance.image_url,
            artist_id=sample_performance.artist_id,
            is_featured=sample_performance.is_featured,
            created_at=sample_performance.created_at,
        )
        mock_repo.update.return_value = updated
        use_case = UpdatePerformance(performance_repo=mock_repo)

        result = await use_case.execute(performance_id=sample_performance.id, title="수정된 콘서트")
        assert result.title == "수정된 콘서트"

    @pytest.mark.asyncio
    async def test_update_not_found(self, mock_repo):
        mock_repo.find_by_id.return_value = None
        use_case = UpdatePerformance(performance_repo=mock_repo)

        with pytest.raises(ValueError, match="공연을 찾을 수 없습니다"):
            await use_case.execute(performance_id=uuid4(), title="수정")

    @pytest.mark.asyncio
    async def test_toggle_featured(self, mock_repo, sample_performance):
        mock_repo.find_by_id.return_value = sample_performance
        toggled = Performance(
            id=sample_performance.id,
            title=sample_performance.title,
            description=sample_performance.description,
            event_date=sample_performance.event_date,
            venue=sample_performance.venue,
            image_url=sample_performance.image_url,
            artist_id=sample_performance.artist_id,
            is_featured=False,
            created_at=sample_performance.created_at,
        )
        mock_repo.update.return_value = toggled
        use_case = UpdatePerformance(performance_repo=mock_repo)

        result = await use_case.execute(performance_id=sample_performance.id, is_featured=False)
        assert result.is_featured is False


class TestDeletePerformance:
    @pytest.mark.asyncio
    async def test_delete_success(self, mock_repo, sample_performance):
        mock_repo.find_by_id.return_value = sample_performance
        use_case = DeletePerformance(performance_repo=mock_repo)

        await use_case.execute(performance_id=sample_performance.id)
        mock_repo.delete.assert_called_once_with(sample_performance.id)

    @pytest.mark.asyncio
    async def test_delete_not_found(self, mock_repo):
        mock_repo.find_by_id.return_value = None
        use_case = DeletePerformance(performance_repo=mock_repo)

        with pytest.raises(ValueError, match="공연을 찾을 수 없습니다"):
            await use_case.execute(performance_id=uuid4())
