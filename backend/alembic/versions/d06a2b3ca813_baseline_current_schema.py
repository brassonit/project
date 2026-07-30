"""baseline_current_schema — 기존 create_tables.sql 스키마를 alembic으로 편입

Revision ID: d06a2b3ca813
Revises:
Create Date: 2026-07-30 12:25:49.302745
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd06a2b3ca813'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# scripts/create_tables.sql 그대로 편입 — CREATE TABLE IF NOT EXISTS / ON CONFLICT DO NOTHING로
# 작성돼 있어 이미 스키마가 적용된 환경(로컬/운영)에서도 안전하게 재실행 가능
_SCHEMA_SQL = """
-- ============================================================
-- BRASSONIT - 연예인 섭외대행 · 공연기획 테이블 생성 스크립트
-- Database: PostgreSQL
-- 기준: design_handoff_brassonit UI (2026-07)
-- ============================================================

CREATE SCHEMA IF NOT EXISTS com;

-- ============================================================
-- ID 생성 함수 — UUID 앞 8자리(hex, 4바이트)
-- ============================================================
CREATE OR REPLACE FUNCTION com.gen_id() RETURNS CHAR(8) AS $$
    SELECT substr(gen_random_uuid()::text, 1, 8);
$$ LANGUAGE sql VOLATILE;

-- ============================================================
-- 1. users (회원)
--    회원가입(이메일+비밀번호, 메일 인증) / 회원정보 수정(이름, 휴대폰) / 탈퇴
-- ============================================================
CREATE TABLE IF NOT EXISTS com.users (
    id                  CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    email               VARCHAR(255)  NOT NULL,
    hashed_password     VARCHAR(255)  NOT NULL,
    name                VARCHAR(100),                          -- 회원정보 수정 화면
    phone               VARCHAR(20),                           -- 회원정보 수정 화면 (하이픈 포맷)
    role                VARCHAR(20)   NOT NULL DEFAULT 'customer',  -- customer | admin
    is_verified         BOOLEAN       NOT NULL DEFAULT FALSE,  -- 이메일 인증 완료 여부
    verification_token  VARCHAR(255),
    created_at          TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP     NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMP                               -- 회원탈퇴 (soft delete)
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_users_email ON com.users (email) WHERE deleted_at IS NULL;

-- ============================================================
-- 2. categories (카테고리) / genres (하위 장르)
--    GNB 탭: 대중가수 · 음악 · 강연 · 사회자 · 퍼포먼스
--    메가메뉴/모바일 칩 바: 아이돌, 발라드, ... (카테고리별 하위 장르)
-- ============================================================
CREATE TABLE IF NOT EXISTS com.categories (
    id          SMALLSERIAL   PRIMARY KEY,
    name        VARCHAR(50)   NOT NULL UNIQUE,
    sort_order  SMALLINT      NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS com.genres (
    id          SMALLSERIAL   PRIMARY KEY,
    category_id SMALLINT      NOT NULL REFERENCES com.categories(id) ON DELETE CASCADE,
    name        VARCHAR(50)   NOT NULL,
    sort_order  SMALLINT      NOT NULL DEFAULT 0,
    UNIQUE (category_id, name)
);

CREATE INDEX IF NOT EXISTS ix_genres_category_id ON com.genres (category_id);

-- ============================================================
-- 3. artists (아티스트)
--    카드: 이름/소개 2줄/좋아요수/조회수, 상세: 장르/인원/소개 + 통계
-- ============================================================
CREATE TABLE IF NOT EXISTS com.artists (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    genre_id    SMALLINT      NOT NULL REFERENCES com.genres(id),   -- 카테고리는 genre → category로 도출
    name        VARCHAR(255)  NOT NULL,
    members     VARCHAR(50),                                        -- 예) 솔로, 5인조
    description TEXT          NOT NULL DEFAULT '',
    like_count  INTEGER       NOT NULL DEFAULT 0,                   -- 비정규화 카운터 (찜과 별개 노출용)
    view_count  BIGINT        NOT NULL DEFAULT 0,
    is_active   BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_artists_genre_id ON com.artists (genre_id);
CREATE INDEX IF NOT EXISTS ix_artists_name ON com.artists (name);

-- 3-1. artist_images — 상세 이미지 슬라이더 (첫 번째가 대표/카드 썸네일)
CREATE TABLE IF NOT EXISTS com.artist_images (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    image_url   VARCHAR(500)  NOT NULL,
    sort_order  SMALLINT      NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_artist_images_artist_id ON com.artist_images (artist_id, sort_order);

-- 3-2. artist_portfolios — 포트폴리오 (그룹: 주요활동/앨범/수상내역/경력사항, 연도 내림차순)
CREATE TABLE IF NOT EXISTS com.artist_portfolios (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    tag         VARCHAR(30)   NOT NULL,      -- 주요활동 | 앨범 | 수상내역 | 경력사항
    year        SMALLINT      NOT NULL,
    content     TEXT          NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_artist_portfolios_artist_id ON com.artist_portfolios (artist_id, tag, year DESC);

-- 3-3. artist_videos — 영상 섹션 (유튜브 embed)
CREATE TABLE IF NOT EXISTS com.artist_videos (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    video_url   VARCHAR(500)  NOT NULL,
    title       VARCHAR(255),
    sort_order  SMALLINT      NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_artist_videos_artist_id ON com.artist_videos (artist_id, sort_order);

-- ============================================================
-- 4. shows (기획공연)
--    홈/목록: 이미지·날짜·제목·한 줄 소개·좋아요·조회, 예정/지난 구분은 event_date로
--    상세: 일시·장소 / 소개 / 출연진 / 예매 링크(예정 공연만)
--         + 공연 소개(문단형, 5줄 접기) / 공연 영상 / 공유 / ♥ 찜 토글
-- ============================================================
CREATE TABLE IF NOT EXISTS com.shows (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    category_id SMALLINT      REFERENCES com.categories(id),
    title       VARCHAR(255)  NOT NULL,
    event_date  DATE          NOT NULL,
    venue       VARCHAR(255)  NOT NULL,
    description TEXT          NOT NULL DEFAULT '',   -- 카드/상세 한 줄 소개
    intro       TEXT          NOT NULL DEFAULT '',   -- 하단 "공연 소개" 본문 (문단은 빈 줄로 구분)
    image_url   VARCHAR(500),
    like_count  INTEGER       NOT NULL DEFAULT 0,    -- 비정규화 카운터 (찜 토글 시 ±1)
    view_count  BIGINT        NOT NULL DEFAULT 0,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- 기존 DB 반영용 (스크립트 재실행 시 안전)
ALTER TABLE com.shows ADD COLUMN IF NOT EXISTS intro TEXT NOT NULL DEFAULT '';

CREATE INDEX IF NOT EXISTS ix_shows_event_date ON com.shows (event_date DESC);

-- 4-1. show_lineups — 출연진 (공연 상세 플레인 텍스트 링크, 견적 공연 첨부 시 자동 첨부)
CREATE TABLE IF NOT EXISTS com.show_lineups (
    show_id     CHAR(8)       NOT NULL REFERENCES com.shows(id) ON DELETE CASCADE,
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    sort_order  SMALLINT      NOT NULL DEFAULT 0,
    PRIMARY KEY (show_id, artist_id)
);

CREATE INDEX IF NOT EXISTS ix_show_lineups_artist_id ON com.show_lineups (artist_id);

-- 4-2. show_tickets — 예매 링크 (회차별 복수, 예정 공연만 존재)
CREATE TABLE IF NOT EXISTS com.show_tickets (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    show_id     CHAR(8)       NOT NULL REFERENCES com.shows(id) ON DELETE CASCADE,
    label       VARCHAR(255)  NOT NULL,   -- 예) 1회차 08.15 (토) — 인터파크 티켓
    url         VARCHAR(500)  NOT NULL,
    sort_order  SMALLINT      NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_show_tickets_show_id ON com.show_tickets (show_id, sort_order);

-- 4-3. show_videos — 공연 영상 섹션 (유튜브 embed, 5개 기본 표시 + 더보기)
CREATE TABLE IF NOT EXISTS com.show_videos (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    show_id     CHAR(8)       NOT NULL REFERENCES com.shows(id) ON DELETE CASCADE,
    video_url   VARCHAR(500)  NOT NULL,
    title       VARCHAR(255),
    sort_order  SMALLINT      NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_show_videos_show_id ON com.show_videos (show_id, sort_order);

-- ============================================================
-- 5. wishlists (찜리스트) / carts (장바구니)
--    로그인 필수. 카드의 하트/장바구니 토글, 찜 → 장바구니 담기
--    찜리스트 화면은 아티스트 테이블 + 공연 테이블(공연 상세 ♥ 찜) 2단 구성
-- ============================================================
CREATE TABLE IF NOT EXISTS com.wishlists (
    user_id     CHAR(8)       NOT NULL REFERENCES com.users(id) ON DELETE CASCADE,
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, artist_id)
);

-- 5-1. show_wishlists — 공연 찜 (공연 상세 ♥ 토글 → 찜리스트 공연 테이블, 문의하기/삭제)
CREATE TABLE IF NOT EXISTS com.show_wishlists (
    user_id     CHAR(8)       NOT NULL REFERENCES com.users(id) ON DELETE CASCADE,
    show_id     CHAR(8)       NOT NULL REFERENCES com.shows(id) ON DELETE CASCADE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, show_id)
);

CREATE TABLE IF NOT EXISTS com.carts (
    user_id     CHAR(8)       NOT NULL REFERENCES com.users(id) ON DELETE CASCADE,
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, artist_id)
);

-- ============================================================
-- 6. quotes (견적)
--    견적 요청(로그인, 장바구니/아티스트 상세) + 견적 문의(비로그인, 이메일 직접 입력)
--    폼: 이메일/이름*/전화번호*/행사명*/행사일(달력 또는 직접입력)/행사지역/내용/첨부/공연 선택
--    견적내역: 일자 | 상태(접수완료→회신완료) | 제목+메타 | 견적서(다운로드/대기중)
-- ============================================================
CREATE TABLE IF NOT EXISTS com.quotes (
    id              CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    user_id         CHAR(8)       REFERENCES com.users(id) ON DELETE SET NULL,  -- NULL = 비로그인 문의
    email           VARCHAR(255)  NOT NULL,   -- 회신 받을 이메일 (로그인 시 가입 이메일 스냅샷)
    name            VARCHAR(100)  NOT NULL,   -- 담당자 이름
    phone           VARCHAR(20)   NOT NULL,
    event_title     VARCHAR(255)  NOT NULL,   -- 행사명
    event_date      DATE,                     -- 달력 선택 시
    event_date_text VARCHAR(100),             -- 직접 입력 시 (예: 미정, 2026년 7월 중순) — 둘 중 하나만 사용
    region          VARCHAR(50),              -- 행사지역 (시/도)
    content         TEXT          NOT NULL DEFAULT '',
    show_id         CHAR(8)       REFERENCES com.shows(id) ON DELETE SET NULL,  -- 첨부된 공연 (출연진 자동 첨부)
    status          VARCHAR(20)   NOT NULL DEFAULT 'received',  -- received(접수완료) | replied(회신완료)
    quote_file_url  VARCHAR(500),             -- 회신완료 시 견적서 파일 (다운로드 버튼)
    replied_at      TIMESTAMP,
    created_at      TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_quotes_user_id ON com.quotes (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_quotes_status ON com.quotes (status);

-- 6-1. quote_artists — 견적에 포함된 아티스트 (선택한 아티스트 n팀 칩)
CREATE TABLE IF NOT EXISTS com.quote_artists (
    quote_id    CHAR(8)       NOT NULL REFERENCES com.quotes(id) ON DELETE CASCADE,
    artist_id   CHAR(8)       NOT NULL REFERENCES com.artists(id) ON DELETE CASCADE,
    PRIMARY KEY (quote_id, artist_id)
);

-- 6-2. quote_attachments — 첨부파일 (복수, 개별 삭제)
CREATE TABLE IF NOT EXISTS com.quote_attachments (
    id          CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    quote_id    CHAR(8)       NOT NULL REFERENCES com.quotes(id) ON DELETE CASCADE,
    file_name   VARCHAR(255)  NOT NULL,
    file_url    VARCHAR(500)  NOT NULL,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_quote_attachments_quote_id ON com.quote_attachments (quote_id);

-- ============================================================
-- 7. policies (이용약관/개인정보취급방침 버전)
--    문서 하단 버전 select — 시행일별 본문 관리
-- ============================================================
CREATE TABLE IF NOT EXISTS com.policies (
    id              CHAR(8)       PRIMARY KEY DEFAULT com.gen_id(),
    policy_type     VARCHAR(20)   NOT NULL,   -- terms | privacy
    effective_date  DATE          NOT NULL,   -- 시행일 (select 옵션)
    content         TEXT          NOT NULL,
    created_at      TIMESTAMP     NOT NULL DEFAULT NOW(),
    UNIQUE (policy_type, effective_date)
);

-- ============================================================
-- SEED DATA — 카테고리/장르 (GNB·메가메뉴 구성)
-- ============================================================
INSERT INTO com.categories (name, sort_order) VALUES
    ('대중가수', 1), ('음악', 2), ('강연', 3), ('사회자', 4), ('퍼포먼스', 5)
ON CONFLICT (name) DO NOTHING;

INSERT INTO com.genres (category_id, name, sort_order)
SELECT c.id, g.name, g.sort_order
FROM (VALUES
    ('대중가수', '아이돌', 1), ('대중가수', '발라드', 2), ('대중가수', '트로트', 3), ('대중가수', '힙합', 4),
    ('음악', '재즈', 1), ('음악', '클래식', 2), ('음악', '뮤지컬', 3), ('음악', '국악', 4),
    ('강연', '셀럽', 1), ('강연', '배우', 2),
    ('사회자', '전문MC', 1), ('사회자', '아나운서', 2),
    ('퍼포먼스', '마술', 1), ('퍼포먼스', '무용', 2), ('퍼포먼스', '댄스', 3)
) AS g(cat_name, name, sort_order)
JOIN com.categories c ON c.name = g.cat_name
ON CONFLICT (category_id, name) DO NOTHING;

-- ----------------------------------------
-- 관리자 계정 (비밀번호: Admin1234! → bcrypt 해시)
-- 견적 등록 알림 메일 수신 계정: brassonitent1016@gmail.com, brassonitent@daum.net
-- ----------------------------------------
INSERT INTO com.users (id, email, hashed_password, role, is_verified, created_at)
VALUES
    ('00000001',
     'admin@brassonit.com',
     '$2b$12$1Txy7xrzjpxdoLC17EZW7.pFB2WlC1hYZeB6wF84y2DgsXIgWUTH6',
     'admin', TRUE, NOW()),
    ('00000002',
     'brassonitent1016@gmail.com',
     '$2b$12$1Txy7xrzjpxdoLC17EZW7.pFB2WlC1hYZeB6wF84y2DgsXIgWUTH6',
     'admin', TRUE, NOW()),
    ('00000003',
     'brassonitent@daum.net',
     '$2b$12$1Txy7xrzjpxdoLC17EZW7.pFB2WlC1hYZeB6wF84y2DgsXIgWUTH6',
     'admin', TRUE, NOW())
ON CONFLICT (id) DO NOTHING;

"""


def upgrade() -> None:
    op.execute(_SCHEMA_SQL)


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS com CASCADE")
