-- ============================================================
-- BRASS ON IT - 연예인 섭외대행 시스템 테이블 생성 스크립트
-- Database: PostgreSQL
-- ============================================================

-- 데이터베이스 생성 (필요 시)
-- CREATE DATABASE celebrity_booking;

-- ============================================================
-- 1. users (회원)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          CHAR(36)        PRIMARY KEY,
    email       VARCHAR(255)    NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role        VARCHAR(20)     NOT NULL DEFAULT 'customer',
    is_verified BOOLEAN         NOT NULL DEFAULT FALSE,
    verification_token VARCHAR(255),
    created_at  TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- ============================================================
-- 2. artists (아티스트)
-- ============================================================
CREATE TABLE IF NOT EXISTS artists (
    id                CHAR(36)      PRIMARY KEY,
    name              VARCHAR(255)  NOT NULL,
    category          VARCHAR(50)   NOT NULL,
    description       TEXT          NOT NULL,
    profile_image_url VARCHAR(500),
    gallery_images    JSONB         NOT NULL DEFAULT '[]'::jsonb,
    is_active         BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at        TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP     NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 3. performances (공연)
-- ============================================================
CREATE TABLE IF NOT EXISTS performances (
    id          CHAR(36)      PRIMARY KEY,
    title       VARCHAR(255)  NOT NULL,
    description TEXT          NOT NULL,
    event_date  DATE          NOT NULL,
    venue       VARCHAR(255)  NOT NULL,
    image_url   VARCHAR(500),
    artist_id   CHAR(36)      REFERENCES artists(id) ON DELETE SET NULL,
    is_featured BOOLEAN       NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_performances_artist_id ON performances (artist_id);
CREATE INDEX IF NOT EXISTS ix_performances_event_date ON performances (event_date);

-- ============================================================
-- 4. inquiries (문의)
-- ============================================================
CREATE TABLE IF NOT EXISTS inquiries (
    id          CHAR(36)      PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(255)  NOT NULL,
    phone       VARCHAR(20),
    subject     VARCHAR(255)  NOT NULL,
    message     TEXT          NOT NULL,
    status      VARCHAR(20)   NOT NULL DEFAULT 'pending',
    admin_reply TEXT,
    created_at  TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_inquiries_status ON inquiries (status);
CREATE INDEX IF NOT EXISTS ix_inquiries_created_at ON inquiries (created_at DESC);
