"""아티스트 API 엔드포인트 통합 테스트"""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from src.infrastructure.database.models import ArtistModel
from src.infrastructure.security.jwt_handler import JWTHandler
from src.main import app


@pytest.fixture
async def client(db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def admin_token(db_session):
    """관리자 JWT 토큰 생성"""
    handler = JWTHandler()
    return handler.create_access_token(user_id=uuid.uuid4(), role="admin")


@pytest.fixture
def user_token(db_session):
    """일반 사용자 JWT 토큰 생성"""
    handler = JWTHandler()
    return handler.create_access_token(user_id=uuid.uuid4(), role="customer")


@pytest.fixture
def sample_artist_data():
    return {
        "name": "김가수",
        "category": "singer",
        "description": "유명한 가수입니다.",
        "profile_image_url": "https://example.com/img.jpg",
        "gallery_images": ["https://example.com/g1.jpg"],
    }


@pytest.fixture
def seed_artists(db_session):
    """테스트용 아티스트 시드 데이터"""
    artists = [
        ArtistModel(
            id=uuid.uuid4(),
            name="김가수",
            category="singer",
            description="가수 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="이댄서",
            category="dancer",
            description="댄서 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="박뮤지션",
            category="musician",
            description="뮤지션 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=True,
        ),
        ArtistModel(
            id=uuid.uuid4(),
            name="최연주자",
            category="instrumentalist",
            description="연주자 설명",
            profile_image_url=None,
            gallery_images=[],
            is_active=False,
        ),
    ]
    for a in artists:
        db_session.add(a)
    db_session.commit()
    return artists


# === 아티스트 목록 조회 (공개) ===


class TestListArtistsAPI:
    @pytest.mark.asyncio
    async def test_list_artists(self, client, seed_artists):
        response = await client.get("/api/artists")
        assert response.status_code == 200
        data = response.json()
        assert "artists" in data
        assert "total" in data
        # 비활성 아티스트는 기본 목록에서 제외
        assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_list_artists_by_category(self, client, seed_artists):
        response = await client.get("/api/artists?category=singer")
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) == 1
        assert data["artists"][0]["category"] == "singer"

    @pytest.mark.asyncio
    async def test_list_artists_invalid_category(self, client):
        response = await client.get("/api/artists?category=invalid")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_list_artists_search(self, client, seed_artists):
        response = await client.get("/api/artists?search=김가수")
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) >= 1
        assert data["artists"][0]["name"] == "김가수"

    @pytest.mark.asyncio
    async def test_list_artists_pagination(self, client, seed_artists):
        response = await client.get("/api/artists?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) == 2
        assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_list_artists_all_categories(self, client, admin_token):
        categories = ["singer", "dancer", "musician", "instrumentalist", "orchestra"]
        for cat in categories:
            await client.post(
                "/api/artists",
                json={
                    "name": f"아티스트_{cat}",
                    "category": cat,
                    "description": f"{cat} 설명",
                },
                headers={"Authorization": f"Bearer {admin_token}"},
            )

        for cat in categories:
            response = await client.get(f"/api/artists?category={cat}")
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1
            assert data["artists"][0]["category"] == cat


# === 아티스트 상세 조회 (공개) ===


class TestGetArtistAPI:
    @pytest.mark.asyncio
    async def test_get_artist_detail(self, client, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.get(f"/api/artists/{artist_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "김가수"
        assert data["category"] == "singer"
        assert data["category_label"] == "대중가수"

    @pytest.mark.asyncio
    async def test_get_artist_not_found(self, client):
        fake_id = str(uuid.uuid4())
        response = await client.get(f"/api/artists/{fake_id}")
        assert response.status_code == 404


# === 아티스트 생성 (관리자 전용) ===


class TestCreateArtistAPI:
    @pytest.mark.asyncio
    async def test_create_artist_as_admin(self, client, admin_token, sample_artist_data):
        response = await client.post(
            "/api/artists",
            json=sample_artist_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "김가수"
        assert data["category"] == "singer"
        assert data["category_label"] == "대중가수"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_artist_as_user_forbidden(self, client, user_token, sample_artist_data):
        response = await client.post(
            "/api/artists",
            json=sample_artist_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_artist_without_auth(self, client, sample_artist_data):
        response = await client.post("/api/artists", json=sample_artist_data)
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_create_artist_invalid_data(self, client, admin_token):
        response = await client.post(
            "/api/artists",
            json={"name": "", "category": "singer", "description": "설명"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_artist_invalid_category(self, client, admin_token):
        response = await client.post(
            "/api/artists",
            json={"name": "테스트", "category": "invalid", "description": "설명"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400


# === 아티스트 수정 (관리자 전용) ===


class TestUpdateArtistAPI:
    @pytest.mark.asyncio
    async def test_update_artist_as_admin(self, client, admin_token, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.put(
            f"/api/artists/{artist_id}",
            json={"name": "김가수 (수정)", "description": "수정된 설명"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "김가수 (수정)"

    @pytest.mark.asyncio
    async def test_update_artist_change_category(self, client, admin_token, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.put(
            f"/api/artists/{artist_id}",
            json={"category": "dancer"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["category"] == "dancer"
        assert response.json()["category_label"] == "댄서"

    @pytest.mark.asyncio
    async def test_update_artist_as_user_forbidden(self, client, user_token, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.put(
            f"/api/artists/{artist_id}",
            json={"name": "수정 시도"},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_artist_not_found(self, client, admin_token):
        fake_id = str(uuid.uuid4())
        response = await client.put(
            f"/api/artists/{fake_id}",
            json={"name": "수정"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_artist_toggle_active(self, client, admin_token, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.put(
            f"/api/artists/{artist_id}",
            json={"is_active": False},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["is_active"] is False


# === 아티스트 삭제 (관리자 전용) ===


class TestDeleteArtistAPI:
    @pytest.mark.asyncio
    async def test_delete_artist_as_admin(self, client, admin_token, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.delete(
            f"/api/artists/{artist_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

        # 삭제 후 조회하면 404
        get_response = await client.get(f"/api/artists/{artist_id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_artist_as_user_forbidden(self, client, user_token, seed_artists):
        artist_id = str(seed_artists[0].id)
        response = await client.delete(
            f"/api/artists/{artist_id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_artist_not_found(self, client, admin_token):
        fake_id = str(uuid.uuid4())
        response = await client.delete(
            f"/api/artists/{fake_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
