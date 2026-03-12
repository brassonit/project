"""아티스트 Use Case 유닛 테스트 (RED Phase)"""

from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from src.application.use_cases.artist.create_artist import CreateArtist
from src.application.use_cases.artist.delete_artist import DeleteArtist
from src.application.use_cases.artist.get_artist import GetArtist
from src.application.use_cases.artist.list_artists import ListArtists
from src.application.use_cases.artist.update_artist import UpdateArtist
from src.domain.entities.artist import Artist
from src.domain.value_objects.artist_category import ArtistCategory

# === Fixtures ===


@pytest.fixture
def mock_artist_repo():
    return AsyncMock()


@pytest.fixture
def sample_artist():
    return Artist(
        id=uuid4(),
        name="김가수",
        category=ArtistCategory.SINGER,
        description="인기 가수입니다.",
        profile_image_url="https://example.com/img.jpg",
        gallery_images=["https://example.com/g1.jpg"],
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_artists():
    return [
        Artist(
            id=uuid4(),
            name="김가수",
            category=ArtistCategory.SINGER,
            description="가수 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Artist(
            id=uuid4(),
            name="이댄서",
            category=ArtistCategory.DANCER,
            description="댄서 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Artist(
            id=uuid4(),
            name="박뮤지션",
            category=ArtistCategory.MUSICIAN,
            description="뮤지션 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]


# === CreateArtist Tests ===


class TestCreateArtist:
    @pytest.mark.asyncio
    async def test_create_artist_success(self, mock_artist_repo, sample_artist):
        mock_artist_repo.save.return_value = sample_artist
        use_case = CreateArtist(artist_repo=mock_artist_repo)

        result = await use_case.execute(
            name="김가수",
            category="singer",
            description="인기 가수입니다.",
            profile_image_url="https://example.com/img.jpg",
            gallery_images=["https://example.com/g1.jpg"],
        )

        assert result.name == "김가수"
        assert result.category == ArtistCategory.SINGER
        mock_artist_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_artist_empty_name_raises(self, mock_artist_repo):
        use_case = CreateArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="이름"):
            await use_case.execute(
                name="",
                category="singer",
                description="설명입니다.",
            )

    @pytest.mark.asyncio
    async def test_create_artist_empty_description_raises(self, mock_artist_repo):
        use_case = CreateArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="설명"):
            await use_case.execute(
                name="김가수",
                category="singer",
                description="",
            )

    @pytest.mark.asyncio
    async def test_create_artist_invalid_category_raises(self, mock_artist_repo):
        use_case = CreateArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="카테고리"):
            await use_case.execute(
                name="김가수",
                category="invalid_category",
                description="설명입니다.",
            )

    @pytest.mark.asyncio
    async def test_create_artist_all_categories(self, mock_artist_repo, sample_artist):
        mock_artist_repo.save.return_value = sample_artist
        use_case = CreateArtist(artist_repo=mock_artist_repo)

        for cat in ["singer", "dancer", "musician", "instrumentalist", "orchestra"]:
            sample_artist.category = ArtistCategory(cat)
            mock_artist_repo.save.return_value = sample_artist
            result = await use_case.execute(
                name="테스트",
                category=cat,
                description="설명입니다.",
            )
            assert result is not None


# === GetArtist Tests ===


class TestGetArtist:
    @pytest.mark.asyncio
    async def test_get_artist_by_id(self, mock_artist_repo, sample_artist):
        mock_artist_repo.find_by_id.return_value = sample_artist
        use_case = GetArtist(artist_repo=mock_artist_repo)

        result = await use_case.execute(artist_id=sample_artist.id)

        assert result.id == sample_artist.id
        assert result.name == "김가수"
        mock_artist_repo.find_by_id.assert_called_once_with(sample_artist.id)

    @pytest.mark.asyncio
    async def test_get_artist_not_found_raises(self, mock_artist_repo):
        mock_artist_repo.find_by_id.return_value = None
        use_case = GetArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="아티스트를 찾을 수 없습니다"):
            await use_case.execute(artist_id=uuid4())


# === ListArtists Tests ===


class TestListArtists:
    @pytest.mark.asyncio
    async def test_list_all_artists(self, mock_artist_repo, sample_artists):
        mock_artist_repo.find_all.return_value = sample_artists
        mock_artist_repo.count_all.return_value = 3
        use_case = ListArtists(artist_repo=mock_artist_repo)

        result = await use_case.execute()

        assert result["total"] == 3
        assert len(result["artists"]) == 3
        mock_artist_repo.find_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_artists_by_category(self, mock_artist_repo, sample_artists):
        singers = [a for a in sample_artists if a.category == ArtistCategory.SINGER]
        mock_artist_repo.find_by_category.return_value = singers
        mock_artist_repo.count_by_category.return_value = 1
        use_case = ListArtists(artist_repo=mock_artist_repo)

        result = await use_case.execute(category="singer")

        assert len(result["artists"]) == 1
        assert result["artists"][0].category == ArtistCategory.SINGER
        mock_artist_repo.find_by_category.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_artists_with_search(self, mock_artist_repo, sample_artists):
        mock_artist_repo.search.return_value = [sample_artists[0]]
        mock_artist_repo.count_search.return_value = 1
        use_case = ListArtists(artist_repo=mock_artist_repo)

        result = await use_case.execute(search="김가수")

        assert len(result["artists"]) == 1
        mock_artist_repo.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_artists_pagination(self, mock_artist_repo, sample_artists):
        mock_artist_repo.find_all.return_value = sample_artists[:2]
        mock_artist_repo.count_all.return_value = 3
        use_case = ListArtists(artist_repo=mock_artist_repo)

        result = await use_case.execute(skip=0, limit=2)

        assert len(result["artists"]) == 2
        assert result["total"] == 3
        mock_artist_repo.find_all.assert_called_once_with(skip=0, limit=2)

    @pytest.mark.asyncio
    async def test_list_artists_invalid_category_raises(self, mock_artist_repo):
        use_case = ListArtists(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="카테고리"):
            await use_case.execute(category="invalid")


# === UpdateArtist Tests ===


class TestUpdateArtist:
    @pytest.mark.asyncio
    async def test_update_artist_success(self, mock_artist_repo, sample_artist):
        mock_artist_repo.find_by_id.return_value = sample_artist
        updated = Artist(
            id=sample_artist.id,
            name="김가수 (수정)",
            category=ArtistCategory.SINGER,
            description="수정된 설명",
            profile_image_url=sample_artist.profile_image_url,
            gallery_images=sample_artist.gallery_images,
            is_active=True,
            created_at=sample_artist.created_at,
            updated_at=datetime.now(),
        )
        mock_artist_repo.update.return_value = updated
        use_case = UpdateArtist(artist_repo=mock_artist_repo)

        result = await use_case.execute(
            artist_id=sample_artist.id,
            name="김가수 (수정)",
            description="수정된 설명",
        )

        assert result.name == "김가수 (수정)"
        mock_artist_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_artist_not_found_raises(self, mock_artist_repo):
        mock_artist_repo.find_by_id.return_value = None
        use_case = UpdateArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="아티스트를 찾을 수 없습니다"):
            await use_case.execute(artist_id=uuid4(), name="수정")

    @pytest.mark.asyncio
    async def test_update_artist_change_category(self, mock_artist_repo, sample_artist):
        mock_artist_repo.find_by_id.return_value = sample_artist
        updated = Artist(
            id=sample_artist.id,
            name=sample_artist.name,
            category=ArtistCategory.DANCER,
            description=sample_artist.description,
            profile_image_url=sample_artist.profile_image_url,
            gallery_images=sample_artist.gallery_images,
            is_active=True,
            created_at=sample_artist.created_at,
            updated_at=datetime.now(),
        )
        mock_artist_repo.update.return_value = updated
        use_case = UpdateArtist(artist_repo=mock_artist_repo)

        result = await use_case.execute(
            artist_id=sample_artist.id,
            category="dancer",
        )

        assert result.category == ArtistCategory.DANCER

    @pytest.mark.asyncio
    async def test_update_artist_invalid_category_raises(self, mock_artist_repo, sample_artist):
        mock_artist_repo.find_by_id.return_value = sample_artist
        use_case = UpdateArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="카테고리"):
            await use_case.execute(
                artist_id=sample_artist.id,
                category="invalid",
            )

    @pytest.mark.asyncio
    async def test_update_artist_toggle_active(self, mock_artist_repo, sample_artist):
        mock_artist_repo.find_by_id.return_value = sample_artist
        deactivated = Artist(
            id=sample_artist.id,
            name=sample_artist.name,
            category=sample_artist.category,
            description=sample_artist.description,
            profile_image_url=sample_artist.profile_image_url,
            gallery_images=sample_artist.gallery_images,
            is_active=False,
            created_at=sample_artist.created_at,
            updated_at=datetime.now(),
        )
        mock_artist_repo.update.return_value = deactivated
        use_case = UpdateArtist(artist_repo=mock_artist_repo)

        result = await use_case.execute(
            artist_id=sample_artist.id,
            is_active=False,
        )

        assert result.is_active is False


# === DeleteArtist Tests ===


class TestDeleteArtist:
    @pytest.mark.asyncio
    async def test_delete_artist_success(self, mock_artist_repo, sample_artist):
        mock_artist_repo.find_by_id.return_value = sample_artist
        use_case = DeleteArtist(artist_repo=mock_artist_repo)

        await use_case.execute(artist_id=sample_artist.id)

        mock_artist_repo.delete.assert_called_once_with(sample_artist.id)

    @pytest.mark.asyncio
    async def test_delete_artist_not_found_raises(self, mock_artist_repo):
        mock_artist_repo.find_by_id.return_value = None
        use_case = DeleteArtist(artist_repo=mock_artist_repo)

        with pytest.raises(ValueError, match="아티스트를 찾을 수 없습니다"):
            await use_case.execute(artist_id=uuid4())
