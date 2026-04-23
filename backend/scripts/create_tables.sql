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

-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- ----------------------------------------
-- users (비밀번호: Admin1234! → bcrypt 해시)
-- ----------------------------------------
INSERT INTO users (id, email, hashed_password, role, is_verified, verification_token, created_at)
VALUES
    ('00000000-0000-0000-0000-000000000001',
     'admin@brassonit.com',
     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQyCgL/OYjdqBMjyMDlODmvJe',
     'admin', TRUE, NULL, NOW()),

    ('00000000-0000-0000-0000-000000000002',
     'customer1@example.com',
     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQyCgL/OYjdqBMjyMDlODmvJe',
     'customer', TRUE, NULL, NOW()),

    ('00000000-0000-0000-0000-000000000003',
     'customer2@example.com',
     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQyCgL/OYjdqBMjyMDlODmvJe',
     'customer', FALSE, 'verify-token-abc123', NOW())
ON CONFLICT (id) DO NOTHING;

-- ----------------------------------------
-- artists
-- ----------------------------------------
INSERT INTO artists (id, name, category, description, profile_image_url, gallery_images, is_active, created_at, updated_at)
VALUES
    ('10000000-0000-0000-0000-000000000001',
     '김수현',
     'singer',
     '대한민국을 대표하는 팝 아티스트. 감성적인 보컬과 퍼포먼스로 수백만 팬을 보유하고 있으며, 기업 행사·시상식·콘서트 등 다양한 무대에서 활약합니다.',
     NULL,
     '[]'::jsonb,
     TRUE, NOW(), NOW()),

    ('10000000-0000-0000-0000-000000000002',
     '박진영 재즈 앙상블',
     'musician',
     '국내 최정상 재즈 뮤지션으로 구성된 5인조 앙상블. 기업 연회, 갈라 디너, 웨딩 리셉션 등 고품격 행사에 최적화된 라이브 공연을 제공합니다.',
     NULL,
     '[]'::jsonb,
     TRUE, NOW(), NOW()),

    ('10000000-0000-0000-0000-000000000003',
     '서울 필하모닉 스트링스',
     'orchestra',
     '클래식부터 팝 크로스오버까지 폭넓은 레퍼토리를 보유한 실내악단. 기업 창립기념일, 시상식, 문화행사에서 품격 있는 연주를 선사합니다.',
     NULL,
     '[]'::jsonb,
     TRUE, NOW(), NOW()),

    ('10000000-0000-0000-0000-000000000004',
     '비트웍스 댄스 크루',
     'dancer',
     'K-POP 및 스트릿 댄스 전문 퍼포먼스 팀. 역동적인 군무와 화려한 무대 연출로 기업 행사 및 축제를 빛내드립니다.',
     NULL,
     '[]'::jsonb,
     TRUE, NOW(), NOW()),

    ('10000000-0000-0000-0000-000000000005',
     '이하은',
     'instrumentalist',
     '국제 콩쿠르 수상 경력의 피아니스트. 클래식 독주회부터 팝 편곡 연주까지 다양한 스타일의 공연이 가능하며, 우아한 분위기의 행사에 어울립니다.',
     NULL,
     '[]'::jsonb,
     FALSE, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- ----------------------------------------
-- performances
-- ----------------------------------------
INSERT INTO performances (id, title, description, event_date, venue, image_url, artist_id, is_featured, created_at)
VALUES
    ('20000000-0000-0000-0000-000000000001',
     '2024 삼성전자 창립기념 갈라 콘서트',
     '삼성전자 창립 55주년 기념 임직원 대상 갈라 콘서트. 김수현의 단독 공연으로 감동의 무대를 연출하였습니다.',
     '2024-11-01',
     '서울 코엑스 오디토리움',
     NULL,
     '10000000-0000-0000-0000-000000000001',
     TRUE, NOW()),

    ('20000000-0000-0000-0000-000000000002',
     '현대자동차 VIP 리셉션 재즈 공연',
     '해외 바이어 초청 VIP 디너 리셉션에서 박진영 재즈 앙상블의 라이브 공연으로 격조 높은 분위기를 연출하였습니다.',
     '2025-02-14',
     '그랜드 인터컨티넨탈 서울 파르나스',
     NULL,
     '10000000-0000-0000-0000-000000000002',
     FALSE, NOW()),

    ('20000000-0000-0000-0000-000000000003',
     '2025 롯데백화점 봄 문화행사',
     '봄 시즌 고객 감사 문화행사로 서울 필하모닉 스트링스의 클래식·크로스오버 공연을 개최하였습니다.',
     '2025-04-05',
     '롯데월드몰 1층 아트리움',
     NULL,
     '10000000-0000-0000-0000-000000000003',
     TRUE, NOW()),

    ('20000000-0000-0000-0000-000000000004',
     'SK그룹 타운홀 미팅 오프닝 퍼포먼스',
     '전사 타운홀 미팅 오프닝 무대를 비트웍스 댄스 크루의 역동적인 퍼포먼스로 장식하였습니다.',
     '2025-06-20',
     'SK T타워 SKY홀',
     NULL,
     '10000000-0000-0000-0000-000000000004',
     FALSE, NOW()),

    ('20000000-0000-0000-0000-000000000005',
     '2025 하반기 기업 시상식 공연',
     '대규모 기업 시상식 축하 공연. 김수현의 특별 무대로 수상자들에게 잊지 못할 순간을 선사할 예정입니다.',
     '2025-12-10',
     'KSPO DOME (올림픽 체조경기장)',
     NULL,
     '10000000-0000-0000-0000-000000000001',
     TRUE, NOW())
ON CONFLICT (id) DO NOTHING;

-- ----------------------------------------
-- inquiries
-- ----------------------------------------
INSERT INTO inquiries (id, name, email, phone, subject, message, status, admin_reply, created_at)
VALUES
    ('30000000-0000-0000-0000-000000000001',
     '이민준',
     'minjun.lee@corp-a.com',
     '010-1234-5678',
     '창립기념 행사 가수 섭외 문의',
     '안녕하세요. 저희 회사 창립 30주년 기념 행사를 준비 중입니다. 300명 규모 행사로 11월 중 개최 예정이며, 인기 가수 섭외가 가능한지 문의드립니다. 예산은 협의 가능합니다.',
     'replied',
     '안녕하세요, 이민준 님. 문의해 주셔서 감사합니다. 말씀하신 일정과 규모에 맞는 아티스트를 제안드릴 수 있습니다. 보다 구체적인 상담을 위해 담당자가 곧 연락드리겠습니다.',
     NOW() - INTERVAL '15 days'),

    ('30000000-0000-0000-0000-000000000002',
     '박서연',
     'seoyeon.park@wedding.com',
     '010-9876-5432',
     '웨딩 리셉션 재즈 밴드 섭외',
     '내년 3월 웨딩 리셉션에서 재즈 공연을 원합니다. 약 2시간 공연 가능한 팀을 추천해 주실 수 있을까요? 장소는 강남구 호텔입니다.',
     'pending',
     NULL,
     NOW() - INTERVAL '3 days'),

    ('30000000-0000-0000-0000-000000000003',
     '최동욱',
     'dongwook.choi@event-pro.co.kr',
     NULL,
     '기업 행사 오케스트라 문의',
     '대기업 VIP 초청 연말 만찬 행사에 실내악단 또는 소규모 오케스트라 섭외를 원합니다. 12월 첫째 주 금요일 저녁, 서울 시내 특급 호텔 연회장입니다. 견적 부탁드립니다.',
     'closed',
     '안녕하세요, 최동욱 님. 해당 일정 확인 결과 서울 필하모닉 스트링스 섭외가 가능합니다. 별도 메일로 견적서를 발송해 드렸으니 확인 부탁드립니다.',
     NOW() - INTERVAL '30 days'),

    ('30000000-0000-0000-0000-000000000004',
     '김하늘',
     'haneul.kim@startup.io',
     '010-5555-7777',
     '스타트업 데모데이 퍼포먼스 팀 문의',
     '스타트업 데모데이 행사 오프닝에 댄스 퍼포먼스 팀을 섭외하고 싶습니다. 100명 규모이며 10~15분 공연을 원합니다. 예산이 많지 않아 부담 없는 옵션이 있는지 궁금합니다.',
     'pending',
     NULL,
     NOW() - INTERVAL '1 day')
ON CONFLICT (id) DO NOTHING;
