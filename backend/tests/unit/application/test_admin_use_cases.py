"""관리자 Use Case 유닛 테스트"""

from unittest.mock import AsyncMock

import pytest
from src.application.use_cases.admin.get_dashboard import GetDashboard


@pytest.fixture
def mock_artist_repo():
    repo = AsyncMock()
    repo.count_all_admin.return_value = 10
    repo.count_all.return_value = 8
    return repo


@pytest.fixture
def mock_performance_repo():
    repo = AsyncMock()
    repo.count_all.return_value = 5
    repo.count_featured.return_value = 2
    return repo


@pytest.fixture
def mock_inquiry_repo():
    repo = AsyncMock()
    repo.count_all.return_value = 15
    repo.count_by_status.side_effect = lambda status: {
        "pending": 7,
        "replied": 5,
        "closed": 3,
    }.get(status.value, 0)
    return repo


class TestGetDashboard:
    @pytest.mark.asyncio
    async def test_dashboard_returns_all_stats(self, mock_artist_repo, mock_performance_repo, mock_inquiry_repo):
        use_case = GetDashboard(
            artist_repo=mock_artist_repo,
            performance_repo=mock_performance_repo,
            inquiry_repo=mock_inquiry_repo,
        )

        result = await use_case.execute()

        assert result["artists"]["total"] == 10
        assert result["artists"]["active"] == 8
        assert result["artists"]["inactive"] == 2
        assert result["performances"]["total"] == 5
        assert result["performances"]["featured"] == 2
        assert result["inquiries"]["total"] == 15
        assert result["inquiries"]["pending"] == 7
        assert result["inquiries"]["replied"] == 5
        assert result["inquiries"]["closed"] == 3

    @pytest.mark.asyncio
    async def test_dashboard_empty_data(self):
        artist_repo = AsyncMock()
        artist_repo.count_all_admin.return_value = 0
        artist_repo.count_all.return_value = 0

        performance_repo = AsyncMock()
        performance_repo.count_all.return_value = 0
        performance_repo.count_featured.return_value = 0

        inquiry_repo = AsyncMock()
        inquiry_repo.count_all.return_value = 0
        inquiry_repo.count_by_status.return_value = 0

        use_case = GetDashboard(
            artist_repo=artist_repo,
            performance_repo=performance_repo,
            inquiry_repo=inquiry_repo,
        )

        result = await use_case.execute()

        assert result["artists"]["total"] == 0
        assert result["performances"]["total"] == 0
        assert result["inquiries"]["total"] == 0
