"""Artist 엔티티 유닛 테스트 (RED Phase)"""

from datetime import datetime
from uuid import uuid4

import pytest
from src.domain.entities.artist import Artist, ArtistCategory


class TestArtistCategory:
    def test_singer_category(self):
        assert ArtistCategory.SINGER == "singer"

    def test_dancer_category(self):
        assert ArtistCategory.DANCER == "dancer"

    def test_musician_category(self):
        assert ArtistCategory.MUSICIAN == "musician"

    def test_instrumentalist_category(self):
        assert ArtistCategory.INSTRUMENTALIST == "instrumentalist"

    def test_orchestra_category(self):
        assert ArtistCategory.ORCHESTRA == "orchestra"

    def test_category_korean_labels(self):
        assert ArtistCategory.SINGER.label_ko == "대중가수"
        assert ArtistCategory.DANCER.label_ko == "댄서"
        assert ArtistCategory.MUSICIAN.label_ko == "뮤지션"
        assert ArtistCategory.INSTRUMENTALIST.label_ko == "연주자"
        assert ArtistCategory.ORCHESTRA.label_ko == "오케스트라"


class TestArtistEntity:
    def test_create_artist_with_valid_data(self):
        artist = Artist(
            id=uuid4(),
            name="홍길동",
            category=ArtistCategory.SINGER,
            description="인기 가수",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert artist.name == "홍길동"
        assert artist.category == ArtistCategory.SINGER
        assert artist.is_active is True

    def test_create_artist_with_all_categories(self):
        for category in ArtistCategory:
            artist = Artist(
                id=uuid4(),
                name=f"아티스트_{category.value}",
                category=category,
                description="설명",
                profile_image_url=None,
                gallery_images=[],
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            assert artist.category == category

    def test_artist_with_gallery_images(self):
        images = ["img1.jpg", "img2.jpg", "img3.jpg"]
        artist = Artist(
            id=uuid4(),
            name="댄서A",
            category=ArtistCategory.DANCER,
            description="댄서 설명",
            profile_image_url="profile.jpg",
            gallery_images=images,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert len(artist.gallery_images) == 3
        assert artist.profile_image_url == "profile.jpg"

    def test_artist_deactivate(self):
        artist = Artist(
            id=uuid4(),
            name="뮤지션B",
            category=ArtistCategory.MUSICIAN,
            description="뮤지션 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        artist.deactivate()
        assert artist.is_active is False

    def test_artist_activate(self):
        artist = Artist(
            id=uuid4(),
            name="연주자C",
            category=ArtistCategory.INSTRUMENTALIST,
            description="연주자 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        artist.activate()
        assert artist.is_active is True

    def test_artist_name_required(self):
        with pytest.raises(ValueError, match="이름"):
            Artist(
                id=uuid4(),
                name="",
                category=ArtistCategory.SINGER,
                description="설명",
                profile_image_url=None,
                gallery_images=[],
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_artist_description_required(self):
        with pytest.raises(ValueError, match="설명"):
            Artist(
                id=uuid4(),
                name="아티스트",
                category=ArtistCategory.SINGER,
                description="",
                profile_image_url=None,
                gallery_images=[],
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
