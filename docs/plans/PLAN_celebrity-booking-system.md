# 구현 계획: 연예인 섭외대행 시스템

**상태**: 🔄 진행 중
**시작일**: 2026-02-12
**최종 업데이트**: 2026-02-13
**예상 완료일**: 2026-02-19

---

**⚠️ 중요 지침**: 각 Phase 완료 후 반드시 수행:
1. ✅ 완료된 작업 체크박스 체크
2. 🧪 모든 품질 게이트 검증 명령 실행
3. ⚠️ 모든 품질 게이트 항목 통과 확인
4. 📅 위의 "최종 업데이트" 날짜 업데이트
5. 📝 학습 내용을 노트 섹션에 문서화
6. ➡️ 그 다음 Phase로 진행

⛔ **품질 게이트를 건너뛰거나 실패한 체크로 진행하지 마세요**

---

## 📋 개요

### 기능 설명
연예인 섭외를 대행하는 온라인 플랫폼입니다. 고객은 카테고리별(대중가수/댄서/뮤지션/연주자/오케스트라) 아티스트를 검색하고, 주요 공연 정보를 확인하며, 섭외 요청 및 문의를 제출할 수 있습니다. 관리자는 관리자 페이지에서 아티스트 정보를 추가/수정할 수 있습니다.

### 성공 기준
- [ ] 이메일 기반 회원가입 및 이메일 인증이 작동함
- [ ] JWT 기반 로그인/로그아웃이 작동함
- [ ] HOME/주요공연/섭외대행/문의하기 메뉴 구조가 반응형으로 구현됨
- [ ] 섭외대행 하위 메뉴(대중가수/댄서/뮤지션/연주자/오케스트라)가 작동함
- [ ] 관리자 페이지에서 섭외대행 정보 추가/수정 가능
- [ ] 반응형 UI가 모바일/태블릿/데스크톱에서 정상 작동
- [ ] 테스트 커버리지 ≥80% (백엔드 비즈니스 로직)

### 사용자 임팩트
- **고객**: 카테고리별 아티스트 탐색 및 섭외 요청을 간편하게 할 수 있음
- **관리자**: 아티스트/공연/문의를 효율적으로 관리 가능
- **플랫폼 운영자**: 자동화된 이메일 인증과 문의 관리로 운영 비용 절감

---

## 🏗️ 아키텍처 결정사항

| 결정사항 | 근거 | 트레이드오프 |
|----------|------|--------------|
| **클린 아키텍처 적용** | 비즈니스 로직과 인프라 분리, 테스트 용이성, 유지보수성 향상 | 초기 설정 복잡도 증가 |
| **FastAPI 백엔드** | 빠른 개발 속도, 자동 문서화(Swagger), 타입 안정성, 비동기 지원 | Python 생태계에 제한 |
| **React + TypeScript 프론트엔드** | 타입 안정성, 컴포넌트 재사용, 풍부한 생태계 | 빌드 설정 복잡도 |
| **Tailwind CSS** | 유틸리티 기반 빠른 개발, 반응형 지원 우수, 커스터마이징 용이 | HTML 클래스가 길어짐 |
| **PostgreSQL** | ACID 보장, JSON 지원, 확장성, 무료 오픈소스 | NoSQL보다 스키마 변경 어려움 |
| **JWT 인증 + 이메일 인증** | Stateless, 확장 가능, 이메일 기반 보안 강화 | Token 무효화 복잡, 이메일 서비스 필요 |
| **SQLAlchemy + Alembic** | ORM 추상화, 마이그레이션 관리, FastAPI와 호환 | 복잡한 쿼리에서 성능 오버헤드 |

---

## 📦 의존성

### 시작 전 필요사항
- [ ] Python 3.11+ 설치
- [ ] Node.js 18+ 및 npm 설치
- [ ] PostgreSQL 14+ 설치 및 실행
- [ ] Git 저장소 초기화

### 외부 의존성

**백엔드 (Python/FastAPI)**:
- fastapi: ^0.109.0
- uvicorn: ^0.27.0
- sqlalchemy: ^2.0.25
- alembic: ^1.13.1
- pydantic: ^2.6.0
- pydantic-settings: ^2.1.0
- python-jose[cryptography]: ^3.3.0 (JWT)
- passlib[bcrypt]: ^1.7.4 (비밀번호 해싱)
- python-multipart: ^0.0.6 (파일 업로드)
- psycopg2-binary: ^2.9.9 (PostgreSQL 드라이버)
- aiosmtplib: ^3.0.0 (이메일 발송)
- jinja2: ^3.1.3 (이메일 템플릿)
- pytest: ^8.0.0
- pytest-cov: ^4.1.0
- pytest-asyncio: ^0.23.4
- httpx: ^0.26.0 (테스트용)

**프론트엔드 (TypeScript/React)**:
- react: ^18.2.0
- react-dom: ^18.2.0
- typescript: ^5.3.3
- vite: ^5.0.11
- tailwindcss: ^3.4.1
- @tanstack/react-query: ^5.17.19
- axios: ^1.6.5
- react-router-dom: ^6.21.3
- @testing-library/react: ^14.1.2
- vitest: ^1.2.1

---

## 🧪 테스트 전략

### 테스팅 접근 방식
**TDD 원칙**: 테스트를 먼저 작성하고, 그 다음 구현

### 이 기능의 테스트 피라미드
| 테스트 타입 | 커버리지 목표 | 목적 |
|-------------|---------------|------|
| **유닛 테스트** | ≥80% | 비즈니스 로직, 도메인 엔티티, Use Cases |
| **통합 테스트** | 주요 경로 | API 엔드포인트, Repository 구현체, DB 연동 |
| **E2E 테스트** | 핵심 사용자 플로우 | 전체 시스템 동작 검증 |

### 테스트 파일 구조
```
backend/
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   │   ├── test_user_entity.py
│   │   │   ├── test_artist_entity.py
│   │   │   ├── test_performance_entity.py
│   │   │   └── test_inquiry_entity.py
│   │   └── application/
│   │       ├── test_auth_use_cases.py
│   │       ├── test_artist_use_cases.py
│   │       ├── test_performance_use_cases.py
│   │       └── test_inquiry_use_cases.py
│   ├── integration/
│   │   ├── test_auth_api.py
│   │   ├── test_artist_api.py
│   │   ├── test_performance_api.py
│   │   ├── test_inquiry_api.py
│   │   └── test_admin_api.py
│   └── conftest.py

frontend/
└── src/
    └── __tests__/
        ├── components/
        ├── features/
        └── pages/
```

### Phase별 커버리지 요구사항
- **Phase 1 (기반)**: 도메인 엔티티 유닛 테스트 (≥80%)
- **Phase 2 (인증)**: 인증 Use Cases + API 통합 테스트 (≥80%)
- **Phase 3 (섭외대행)**: 아티스트 CRUD + 카테고리 필터 테스트 (≥80%)
- **Phase 4 (공연/문의)**: 공연/문의 비즈니스 로직 + API 테스트 (≥80%)
- **Phase 5 (관리자)**: 관리자 API 테스트 (≥80%)
- **Phase 6 (프론트엔드)**: 주요 컴포넌트 렌더링 테스트 (≥60%)
- **Phase 7 (통합)**: E2E 플로우 테스트

---

## 🚀 구현 Phase

### Phase 1: 프로젝트 기반 구조 및 도메인 모델
**목표**: 클린 아키텍처 기반 프로젝트 구조를 설정하고, 핵심 도메인 엔티티를 구현
**예상 시간**: 3-4 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 1.1**: User 엔티티 유닛 테스트 작성
  - 파일: `backend/tests/unit/domain/test_user_entity.py`
  - 예상: 테스트 실패 (red) - User 엔티티가 아직 존재하지 않음
  - 상세:
    - 사용자 생성 (이메일, 비밀번호, 역할)
    - 비밀번호 해싱 검증
    - 이메일 유효성 검증
    - 역할 타입 (customer, admin) 검증
    - 이메일 인증 상태 관리 (is_verified)

- [ ] **Test 1.2**: Artist 엔티티 유닛 테스트 작성
  - 파일: `backend/tests/unit/domain/test_artist_entity.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 아티스트 프로필 생성 (이름, 카테고리, 설명, 이미지)
    - 카테고리 유효성 (singer, dancer, musician, instrumentalist, orchestra)
    - 프로필 필드 검증

- [ ] **Test 1.3**: Performance 엔티티 유닛 테스트 작성
  - 파일: `backend/tests/unit/domain/test_performance_entity.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 공연 정보 생성 (제목, 설명, 날짜, 장소, 이미지)
    - 날짜 유효성 검증
    - 필수 필드 검증

- [ ] **Test 1.4**: Inquiry 엔티티 유닛 테스트 작성
  - 파일: `backend/tests/unit/domain/test_inquiry_entity.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 문의 생성 (이름, 이메일, 전화, 제목, 내용)
    - 문의 상태 (pending, replied, closed)
    - 필수 필드 검증

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 1.5**: 프로젝트 디렉토리 구조 생성
  - 파일: 전체 프로젝트 구조
  - 목표: 클린 아키텍처 레이어 구성
  - 상세:
    ```
    backend/
    ├── src/
    │   ├── domain/
    │   │   ├── entities/
    │   │   │   ├── __init__.py
    │   │   │   ├── user.py
    │   │   │   ├── artist.py
    │   │   │   ├── performance.py
    │   │   │   └── inquiry.py
    │   │   ├── repositories/
    │   │   │   ├── __init__.py
    │   │   │   ├── user_repository.py
    │   │   │   ├── artist_repository.py
    │   │   │   ├── performance_repository.py
    │   │   │   └── inquiry_repository.py
    │   │   └── value_objects/
    │   │       ├── __init__.py
    │   │       ├── email.py
    │   │       └── artist_category.py
    │   ├── application/
    │   │   ├── use_cases/
    │   │   └── dto/
    │   ├── infrastructure/
    │   │   ├── database/
    │   │   ├── repositories/
    │   │   ├── security/
    │   │   └── email/
    │   └── presentation/
    │       ├── api/
    │       └── schemas/
    ├── tests/
    ├── alembic/
    ├── pyproject.toml
    └── pytest.ini

    frontend/
    ├── src/
    │   ├── domain/
    │   │   └── models/
    │   ├── application/
    │   │   └── hooks/
    │   ├── infrastructure/
    │   │   ├── api/
    │   │   └── auth/
    │   └── presentation/
    │       ├── components/
    │       │   ├── common/
    │       │   ├── layout/
    │       │   └── ui/
    │       ├── pages/
    │       │   ├── home/
    │       │   ├── performances/
    │       │   ├── booking/
    │       │   │   ├── singers/
    │       │   │   ├── dancers/
    │       │   │   ├── musicians/
    │       │   │   ├── instrumentalists/
    │       │   │   └── orchestra/
    │       │   ├── inquiry/
    │       │   ├── auth/
    │       │   └── admin/
    │       └── layouts/
    ├── public/
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    └── tailwind.config.js
    ```

- [ ] **Task 1.6**: Python 의존성 설정
  - 파일: `backend/pyproject.toml`, `backend/requirements.txt`
  - 목표: 필요한 패키지 설치 설정
  - 상세: FastAPI, SQLAlchemy, Alembic, pytest, aiosmtplib 등

- [ ] **Task 1.7**: User 도메인 엔티티 구현
  - 파일: `backend/src/domain/entities/user.py`
  - 목표: Test 1.1 통과
  - 상세:
    ```python
    @dataclass
    class User:
        id: Optional[UUID]
        email: str
        hashed_password: str
        role: UserRole  # customer, admin
        is_verified: bool  # 이메일 인증 여부
        verification_token: Optional[str]
        created_at: datetime
    ```

- [ ] **Task 1.8**: Artist 도메인 엔티티 구현
  - 파일: `backend/src/domain/entities/artist.py`
  - 목표: Test 1.2 통과
  - 상세:
    ```python
    class ArtistCategory(str, Enum):
        SINGER = "singer"           # 대중가수
        DANCER = "dancer"           # 댄서
        MUSICIAN = "musician"       # 뮤지션
        INSTRUMENTALIST = "instrumentalist"  # 연주자
        ORCHESTRA = "orchestra"     # 오케스트라

    @dataclass
    class Artist:
        id: Optional[UUID]
        name: str
        category: ArtistCategory
        description: str
        profile_image_url: Optional[str]
        gallery_images: list[str]
        is_active: bool
        created_at: datetime
        updated_at: datetime
    ```

- [ ] **Task 1.9**: Performance 도메인 엔티티 구현
  - 파일: `backend/src/domain/entities/performance.py`
  - 목표: Test 1.3 통과
  - 상세:
    ```python
    @dataclass
    class Performance:
        id: Optional[UUID]
        title: str
        description: str
        event_date: date
        venue: str
        image_url: Optional[str]
        artist_id: Optional[UUID]
        is_featured: bool
        created_at: datetime
    ```

- [ ] **Task 1.10**: Inquiry 도메인 엔티티 구현
  - 파일: `backend/src/domain/entities/inquiry.py`
  - 목표: Test 1.4 통과
  - 상세:
    ```python
    class InquiryStatus(str, Enum):
        PENDING = "pending"
        REPLIED = "replied"
        CLOSED = "closed"

    @dataclass
    class Inquiry:
        id: Optional[UUID]
        name: str
        email: str
        phone: Optional[str]
        subject: str
        message: str
        status: InquiryStatus
        admin_reply: Optional[str]
        created_at: datetime
    ```

- [ ] **Task 1.11**: Repository 인터페이스 정의
  - 파일: `backend/src/domain/repositories/*.py`
  - 목표: 각 엔티티별 Repository 인터페이스 (ABC)
  - 상세:
    - `IUserRepository`: save, find_by_id, find_by_email, find_by_verification_token
    - `IArtistRepository`: save, find_by_id, find_all, find_by_category, search, delete
    - `IPerformanceRepository`: save, find_by_id, find_all, find_featured, delete
    - `IInquiryRepository`: save, find_by_id, find_all, update_status, delete

- [ ] **Task 1.12**: PostgreSQL 스키마 설계 및 Alembic 마이그레이션
  - 파일: `alembic/versions/001_initial_schema.py`
  - 목표: 데이터베이스 테이블 생성
  - 상세:
    - users 테이블 (id, email, hashed_password, role, is_verified, verification_token, created_at)
    - artists 테이블 (id, name, category, description, profile_image_url, gallery_images, is_active, created_at, updated_at)
    - performances 테이블 (id, title, description, event_date, venue, image_url, artist_id, is_featured, created_at)
    - inquiries 테이블 (id, name, email, phone, subject, message, status, admin_reply, created_at)

- [ ] **Task 1.13**: React 프론트엔드 프로젝트 초기 설정
  - 파일: `frontend/` 전체
  - 목표: Vite + React + TypeScript + Tailwind CSS 설정
  - 상세:
    - Vite 프로젝트 생성
    - Tailwind CSS 설정
    - 기본 디렉토리 구조 생성

**🔵 REFACTOR: 코드 품질 개선**
- [ ] **Task 1.14**: 코드 리팩토링 및 품질 개선
  - 파일: 이 Phase의 모든 새 코드 검토
  - 목표: 테스트를 깨지 않으면서 설계 개선
  - 체크리스트:
    - [ ] 중복 제거 (DRY 원칙)
    - [ ] Value Objects 추출 (Email, ArtistCategory)
    - [ ] Type hints 완성
    - [ ] Docstring 추가

#### Quality Gate ✋

**⚠️ 중지: Phase 2로 진행하기 전에 모든 체크 통과 필수**

**TDD 준수** (중요):
- [ ] **Red Phase**: 테스트를 먼저 작성하고 초기 실패 확인
- [ ] **Green Phase**: 테스트를 통과하는 프로덕션 코드 작성
- [ ] **Refactor Phase**: 테스트가 여전히 통과하는 상태에서 코드 개선
- [ ] **커버리지 확인**: 테스트 커버리지 ≥80%

**빌드 & 테스트**:
- [ ] **빌드**: 프로젝트가 오류 없이 빌드됨
- [ ] **모든 테스트 통과**: 100% 테스트 통과
- [ ] **Flaky 테스트 없음**: 3회 이상 일관되게 통과

**코드 품질**:
- [ ] **린팅**: `ruff check src tests`
- [ ] **포매팅**: `black --check src tests`
- [ ] **타입 안정성**: `mypy src`

**검증 명령어**:
```bash
cd backend
pytest -v --cov=src --cov-report=term-missing
ruff check src tests
black --check src tests
mypy src
alembic upgrade head
```

---

### Phase 2: 사용자 인증 시스템 (이메일 인증 포함)
**목표**: 이메일 기반 회원가입, 이메일 인증, JWT 로그인/로그아웃 구현
**예상 시간**: 3-4 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 2.1**: 회원가입 Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_auth_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 유효한 이메일로 회원가입 성공
    - 이메일 중복 시 실패
    - 약한 비밀번호 거부
    - 잘못된 이메일 형식 거부
    - 회원가입 시 인증 이메일 발송 확인
    - 회원가입 직후 is_verified = False

- [ ] **Test 2.2**: 이메일 인증 Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_auth_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 유효한 인증 토큰으로 이메일 인증 성공
    - 만료된 토큰으로 인증 실패
    - 잘못된 토큰으로 인증 실패
    - 이미 인증된 사용자 재인증 시도

- [ ] **Test 2.3**: 로그인 Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_auth_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 인증된 사용자 로그인 성공 + JWT 반환
    - 미인증 사용자 로그인 시 이메일 인증 요구
    - 잘못된 비밀번호로 로그인 실패
    - 존재하지 않는 이메일로 로그인 실패

- [ ] **Test 2.4**: 인증 API 엔드포인트 통합 테스트
  - 파일: `backend/tests/integration/test_auth_api.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - POST /api/auth/register
    - GET /api/auth/verify-email?token=xxx
    - POST /api/auth/login
    - GET /api/auth/me
    - POST /api/auth/resend-verification

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 2.5**: UserRepository 구현 (SQLAlchemy)
  - 파일: `backend/src/infrastructure/repositories/user_repository.py`
  - 목표: IUserRepository 인터페이스 구현

- [ ] **Task 2.6**: 비밀번호 해싱 서비스
  - 파일: `backend/src/infrastructure/security/password_hasher.py`
  - 목표: bcrypt 기반 해싱/검증

- [ ] **Task 2.7**: JWT 토큰 서비스
  - 파일: `backend/src/infrastructure/security/jwt_handler.py`
  - 목표: Access token + Refresh token 생성/검증

- [ ] **Task 2.8**: 이메일 발송 서비스
  - 파일: `backend/src/infrastructure/email/email_service.py`
  - 목표: 인증 이메일 발송 (SMTP)
  - 상세:
    - 인증 이메일 템플릿 (Jinja2)
    - 인증 링크 생성 (토큰 기반)
    - SMTP 설정 (환경변수)

- [ ] **Task 2.9**: 회원가입 Use Case 구현
  - 파일: `backend/src/application/use_cases/auth/register_user.py`
  - 목표: Test 2.1 통과
  - 상세: 이메일 중복 확인 → 비밀번호 해싱 → 사용자 생성 → 인증 이메일 발송

- [ ] **Task 2.10**: 이메일 인증 Use Case 구현
  - 파일: `backend/src/application/use_cases/auth/verify_email.py`
  - 목표: Test 2.2 통과
  - 상세: 토큰 검증 → is_verified = True

- [ ] **Task 2.11**: 로그인 Use Case 구현
  - 파일: `backend/src/application/use_cases/auth/login_user.py`
  - 목표: Test 2.3 통과
  - 상세: 이메일 확인 → 인증 상태 확인 → 비밀번호 검증 → JWT 발급

- [ ] **Task 2.12**: FastAPI 인증 라우터 구현
  - 파일: `backend/src/presentation/api/auth.py`
  - 목표: Test 2.4 통과
  - 상세:
    - POST /api/auth/register
    - GET /api/auth/verify-email
    - POST /api/auth/login
    - GET /api/auth/me
    - POST /api/auth/resend-verification

- [ ] **Task 2.13**: 인증 미들웨어 및 의존성
  - 파일: `backend/src/presentation/dependencies/auth.py`
  - 목표: JWT 검증 + 현재 사용자 주입 + 관리자 권한 확인

**🔵 REFACTOR: 코드 품질 개선**
- [ ] **Task 2.14**: 인증 코드 리팩토링
  - 체크리스트:
    - [ ] Custom exceptions 정의
    - [ ] 비밀번호 정책 상수화
    - [ ] JWT/이메일 설정 환경변수 분리
    - [ ] 로깅 추가

#### Quality Gate ✋

**⚠️ 중지: Phase 3로 진행하기 전에 모든 체크 통과 필수**

**TDD 준수**:
- [ ] Red-Green-Refactor 사이클 준수
- [ ] 인증 모듈 커버리지 ≥80%

**빌드 & 테스트**:
- [ ] Phase 1 + Phase 2 모든 테스트 통과
- [ ] API 엔드포인트 정상 작동 (Swagger /docs 확인)

**보안**:
- [ ] 비밀번호 평문 저장 없음
- [ ] JWT 토큰에 민감 정보 미포함
- [ ] 이메일 인증 토큰 안전한 생성

**검증 명령어**:
```bash
cd backend
pytest -v --cov=src --cov-report=term-missing
ruff check src tests && black --check src tests && mypy src
uvicorn src.main:app --reload  # http://localhost:8000/docs 확인
```

---

### Phase 3: 섭외대행 아티스트 관리
**목표**: 카테고리별(대중가수/댄서/뮤지션/연주자/오케스트라) 아티스트 CRUD 및 조회 기능 구현
**예상 시간**: 3-4 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 3.1**: 아티스트 CRUD Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_artist_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 아티스트 생성 (관리자만)
    - 아티스트 조회 (모든 사용자)
    - 아티스트 수정 (관리자만)
    - 아티스트 삭제 (관리자만)
    - 카테고리별 필터링

- [ ] **Test 3.2**: 아티스트 검색/필터 Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_artist_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 카테고리별 필터링 (singer, dancer, musician, instrumentalist, orchestra)
    - 이름 검색
    - 활성/비활성 필터링
    - 페이지네이션

- [ ] **Test 3.3**: 아티스트 API 엔드포인트 통합 테스트
  - 파일: `backend/tests/integration/test_artist_api.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - GET /api/artists (목록, 필터)
    - GET /api/artists?category=singer (카테고리별)
    - GET /api/artists/{id} (상세)
    - POST /api/artists (생성, 관리자)
    - PUT /api/artists/{id} (수정, 관리자)
    - DELETE /api/artists/{id} (삭제, 관리자)

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 3.4**: ArtistRepository 구현
  - 파일: `backend/src/infrastructure/repositories/artist_repository.py`
  - 목표: IArtistRepository 인터페이스 구현
  - 상세: CRUD + 카테고리 필터 + 검색 + 페이지네이션

- [ ] **Task 3.5**: 아티스트 CRUD Use Cases
  - 파일: `backend/src/application/use_cases/artist/`
  - 목표: Test 3.1, 3.2 통과
  - 상세:
    - create_artist.py: 관리자 권한 확인, 유효성 검증, 저장
    - get_artist.py: ID로 조회
    - list_artists.py: 목록 + 카테고리 필터 + 검색 + 페이지네이션
    - update_artist.py: 관리자 권한 확인, 수정
    - delete_artist.py: 관리자 권한 확인, 삭제

- [ ] **Task 3.6**: FastAPI 아티스트 라우터 구현
  - 파일: `backend/src/presentation/api/artists.py`
  - 목표: Test 3.3 통과

- [ ] **Task 3.7**: Pydantic 스키마 정의
  - 파일: `backend/src/presentation/schemas/artist.py`
  - 상세: ArtistCreate, ArtistUpdate, ArtistResponse, ArtistListParams

**🔵 REFACTOR: 코드 품질 개선**
- [ ] **Task 3.8**: 아티스트 모듈 리팩토링
  - 체크리스트:
    - [ ] 카테고리 한글 매핑 추가 (singer→대중가수)
    - [ ] 검색 쿼리 최적화
    - [ ] 권한 체크 중복 제거
    - [ ] 에러 메시지 개선

#### Quality Gate ✋

**TDD 준수**:
- [ ] Red-Green-Refactor 사이클 준수
- [ ] 아티스트 모듈 커버리지 ≥80%

**빌드 & 테스트**:
- [ ] Phase 1-3 모든 테스트 통과
- [ ] 카테고리별 필터링 정상 작동

**검증 명령어**:
```bash
cd backend
pytest -v --cov=src --cov-report=term-missing
ruff check src tests && black --check src tests && mypy src
# API 테스트
curl http://localhost:8000/api/artists?category=singer
curl http://localhost:8000/api/artists?category=dancer
```

---

### Phase 4: 주요공연 & 문의하기
**목표**: 주요 공연 정보 관리 및 문의 폼 기능 구현
**예상 시간**: 2-3 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 4.1**: 공연 CRUD Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_performance_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 공연 생성 (관리자만)
    - 공연 목록 조회 (모든 사용자)
    - 주요 공연 (is_featured) 필터링
    - 공연 수정/삭제 (관리자만)

- [ ] **Test 4.2**: 문의 Use Case 유닛 테스트
  - 파일: `backend/tests/unit/application/test_inquiry_use_cases.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 문의 생성 (비로그인 가능)
    - 문의 목록 조회 (관리자만)
    - 문의 답변 (관리자만)
    - 문의 상태 변경

- [ ] **Test 4.3**: 공연/문의 API 통합 테스트
  - 파일: `backend/tests/integration/test_performance_api.py`, `test_inquiry_api.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - GET /api/performances (목록)
    - GET /api/performances/featured (주요 공연)
    - POST /api/performances (관리자)
    - POST /api/inquiries (문의 제출)
    - GET /api/inquiries (관리자 목록)
    - PATCH /api/inquiries/{id}/reply (관리자 답변)

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 4.4**: PerformanceRepository 및 InquiryRepository 구현
- [ ] **Task 4.5**: 공연 Use Cases 구현
- [ ] **Task 4.6**: 문의 Use Cases 구현
- [ ] **Task 4.7**: FastAPI 공연/문의 라우터 구현
- [ ] **Task 4.8**: Pydantic 스키마 정의

**🔵 REFACTOR: 코드 품질 개선**
- [ ] **Task 4.9**: 코드 리팩토링

#### Quality Gate ✋

**TDD 준수**:
- [ ] Red-Green-Refactor 사이클 준수
- [ ] 공연/문의 모듈 커버리지 ≥80%

**빌드 & 테스트**:
- [ ] Phase 1-4 모든 테스트 통과

**검증 명령어**:
```bash
cd backend
pytest -v --cov=src --cov-report=term-missing
ruff check src tests && black --check src tests && mypy src
```

---

### Phase 5: 관리자 페이지 API
**목표**: 관리자 전용 API로 섭외대행 정보 추가/수정, 공연/문의 관리 기능 구현
**예상 시간**: 2-3 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 5.1**: 관리자 대시보드 API 통합 테스트
  - 파일: `backend/tests/integration/test_admin_api.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - GET /api/admin/dashboard (통계: 아티스트 수, 공연 수, 문의 수)
    - GET /api/admin/artists (관리자용 아티스트 목록, 비활성 포함)
    - GET /api/admin/inquiries (모든 문의 목록 + 상태 필터)
    - GET /api/admin/performances (모든 공연 관리)
    - 비관리자 접근 시 403 반환

- [ ] **Test 5.2**: 관리자 벌크 작업 테스트
  - 파일: `backend/tests/integration/test_admin_api.py`
  - 예상: 테스트 실패 (red)
  - 상세:
    - 이미지 업로드 API (아티스트 프로필/갤러리)
    - 아티스트 활성/비활성 토글
    - 공연 주요 공연 토글

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 5.3**: 관리자 대시보드 Use Case
  - 파일: `backend/src/application/use_cases/admin/get_dashboard.py`
  - 목표: 통계 데이터 집계

- [ ] **Task 5.4**: 이미지 업로드 서비스
  - 파일: `backend/src/infrastructure/storage/file_storage.py`
  - 목표: 로컬 파일 저장소 (추후 S3 전환 가능)

- [ ] **Task 5.5**: FastAPI 관리자 라우터 구현
  - 파일: `backend/src/presentation/api/admin.py`
  - 목표: 관리자 전용 엔드포인트 (require_admin 의존성)

- [ ] **Task 5.6**: 초기 관리자 계정 시딩
  - 파일: `backend/src/infrastructure/database/seed.py`
  - 목표: 기본 관리자 계정 생성 스크립트

**🔵 REFACTOR: 코드 품질 개선**
- [ ] **Task 5.7**: 관리자 모듈 리팩토링

#### Quality Gate ✋

**TDD 준수**:
- [ ] Red-Green-Refactor 사이클 준수
- [ ] 관리자 API 커버리지 ≥80%

**보안**:
- [ ] 관리자 전용 엔드포인트에 권한 검증 적용
- [ ] 파일 업로드 유효성 검증 (크기, 타입 제한)

**검증 명령어**:
```bash
cd backend
pytest -v --cov=src --cov-report=term-missing
ruff check src tests && black --check src tests && mypy src
```

---

### Phase 6: React 프론트엔드 UI (반응형)
**목표**: 반응형 UI 구현 - HOME/주요공연/섭외대행/문의하기 메뉴 구조 + 관리자 페이지
**예상 시간**: 4-5 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 6.1**: 레이아웃/네비게이션 컴포넌트 테스트
  - 파일: `frontend/src/__tests__/components/layout/`
  - 상세:
    - 헤더 네비게이션 렌더링 (HOME/주요공연/섭외대행/문의하기)
    - 섭외대행 드롭다운 메뉴 (대중가수/댄서/뮤지션/연주자/오케스트라)
    - 모바일 햄버거 메뉴
    - 로그인/로그아웃 버튼 상태

- [ ] **Test 6.2**: 인증 페이지 컴포넌트 테스트
  - 파일: `frontend/src/__tests__/pages/auth/`
  - 상세:
    - 로그인 폼 렌더링 및 제출
    - 회원가입 폼 렌더링 및 제출
    - 이메일 인증 안내 페이지

- [ ] **Test 6.3**: 주요 페이지 컴포넌트 테스트
  - 파일: `frontend/src/__tests__/pages/`
  - 상세:
    - HOME 페이지 렌더링
    - 주요공연 목록 페이지
    - 섭외대행 카테고리 페이지
    - 아티스트 상세 페이지
    - 문의하기 폼 페이지

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 6.4**: API 클라이언트 설정
  - 파일: `frontend/src/infrastructure/api/client.ts`
  - 상세: Axios 인스턴스, JWT 인터셉터, 에러 핸들링

- [ ] **Task 6.5**: 인증 Context/Hook
  - 파일: `frontend/src/infrastructure/auth/AuthContext.tsx`
  - 상세: useAuth hook, login/logout/register, 토큰 관리

- [ ] **Task 6.6**: 공통 레이아웃 구현
  - 파일: `frontend/src/presentation/layouts/`
  - 상세:
    - MainLayout.tsx: 헤더 + 푸터 + 컨텐츠
    - Header.tsx: 로고, 메뉴 (HOME/주요공연/섭외대행/문의하기)
    - 섭외대행 드롭다운: 대중가수/댄서/뮤지션/연주자/오케스트라
    - 모바일 반응형 햄버거 메뉴
    - Footer.tsx: 회사 정보, 연락처

- [ ] **Task 6.7**: HOME 페이지
  - 파일: `frontend/src/presentation/pages/home/HomePage.tsx`
  - 상세:
    - 히어로 배너
    - 주요 공연 하이라이트
    - 카테고리별 아티스트 미리보기
    - CTA (섭외 요청하기)

- [ ] **Task 6.8**: 주요공연 페이지
  - 파일: `frontend/src/presentation/pages/performances/`
  - 상세:
    - PerformanceListPage.tsx: 공연 카드 리스트
    - PerformanceDetailPage.tsx: 공연 상세 정보

- [ ] **Task 6.9**: 섭외대행 페이지 (카테고리별)
  - 파일: `frontend/src/presentation/pages/booking/`
  - 상세:
    - BookingCategoryPage.tsx: 카테고리 공통 레이아웃
    - ArtistListByCategory.tsx: 카테고리별 아티스트 목록
    - ArtistDetailPage.tsx: 아티스트 상세 + 섭외 문의 버튼
    - 라우팅:
      - /booking/singers → 대중가수
      - /booking/dancers → 댄서
      - /booking/musicians → 뮤지션
      - /booking/instrumentalists → 연주자
      - /booking/orchestra → 오케스트라

- [ ] **Task 6.10**: 문의하기 페이지
  - 파일: `frontend/src/presentation/pages/inquiry/InquiryPage.tsx`
  - 상세:
    - 이름, 이메일, 전화, 제목, 내용 입력 폼
    - 유효성 검증
    - 전송 성공/실패 안내

- [ ] **Task 6.11**: 인증 페이지
  - 파일: `frontend/src/presentation/pages/auth/`
  - 상세:
    - LoginPage.tsx: 이메일/비밀번호 로그인
    - RegisterPage.tsx: 이메일 회원가입
    - VerifyEmailPage.tsx: 이메일 인증 완료 페이지
    - EmailSentPage.tsx: 인증 이메일 발송 안내

- [ ] **Task 6.12**: 관리자 페이지
  - 파일: `frontend/src/presentation/pages/admin/`
  - 상세:
    - AdminDashboard.tsx: 대시보드 (통계)
    - AdminArtists.tsx: 아티스트 목록 + 추가/수정/삭제
    - AdminArtistForm.tsx: 아티스트 추가/수정 폼 (이미지 업로드)
    - AdminPerformances.tsx: 공연 관리
    - AdminInquiries.tsx: 문의 관리 + 답변

- [ ] **Task 6.13**: React Router 설정
  - 파일: `frontend/src/App.tsx`
  - 상세:
    ```
    /                       → HOME
    /performances           → 주요공연 목록
    /performances/:id       → 공연 상세
    /booking/singers        → 대중가수
    /booking/dancers        → 댄서
    /booking/musicians      → 뮤지션
    /booking/instrumentalists → 연주자
    /booking/orchestra      → 오케스트라
    /booking/artist/:id     → 아티스트 상세
    /inquiry                → 문의하기
    /login                  → 로그인
    /register               → 회원가입
    /verify-email           → 이메일 인증
    /admin                  → 관리자 대시보드 (Protected)
    /admin/artists          → 아티스트 관리 (Protected)
    /admin/artists/new      → 아티스트 추가 (Protected)
    /admin/artists/:id/edit → 아티스트 수정 (Protected)
    /admin/performances     → 공연 관리 (Protected)
    /admin/inquiries        → 문의 관리 (Protected)
    ```

**🔵 REFACTOR: 코드 품질 개선**
- [ ] **Task 6.14**: 프론트엔드 리팩토링
  - 체크리스트:
    - [ ] 공통 컴포넌트 추출 (Button, Input, Card, Modal)
    - [ ] Tailwind 반응형 검증 (sm, md, lg, xl)
    - [ ] 로딩/에러 상태 컴포넌트
    - [ ] 접근성 개선 (a11y)

#### Quality Gate ✋

**TDD 준수**:
- [ ] Red-Green-Refactor 사이클 준수
- [ ] 주요 컴포넌트 커버리지 ≥60%

**빌드 & 테스트**:
- [ ] `npm run build` 성공
- [ ] `npm test` 모든 테스트 통과
- [ ] `npm run lint` 오류 없음
- [ ] `tsc --noEmit` 타입 체크 통과

**반응형 검증**:
- [ ] 모바일 (375px) 정상 작동
- [ ] 태블릿 (768px) 정상 작동
- [ ] 데스크톱 (1280px) 정상 작동
- [ ] 햄버거 메뉴 작동 확인

**검증 명령어**:
```bash
cd frontend
npm install && npm run build
npm test
npm run lint
tsc --noEmit
npm run dev  # http://localhost:5173 확인
```

---

### Phase 7: 통합 테스트 & 마무리
**목표**: 프론트-백엔드 연동 검증, 반응형 최종 검증, 배포 준비
**예상 시간**: 2-3 시간
**상태**: ⏳ 대기 중

#### 작업

**🔴 RED: 실패하는 테스트 먼저 작성**
- [ ] **Test 7.1**: E2E 핵심 플로우 테스트
  - 상세:
    - 회원가입 → 이메일 인증 → 로그인 플로우
    - 아티스트 카테고리 탐색 플로우
    - 문의하기 제출 플로우
    - 관리자 아티스트 추가/수정 플로우

**🟢 GREEN: 테스트를 통과하는 구현**
- [ ] **Task 7.2**: CORS 설정 및 프론트-백 연동 검증
  - 파일: `backend/src/main.py`
  - 상세: CORS 미들웨어, API 프록시 설정

- [ ] **Task 7.3**: 환경변수 및 설정 분리
  - 파일: `.env.example`, `backend/src/infrastructure/config.py`
  - 상세:
    - DATABASE_URL
    - JWT_SECRET_KEY
    - SMTP 설정 (HOST, PORT, USER, PASSWORD)
    - FRONTEND_URL (이메일 인증 링크용)

- [ ] **Task 7.4**: Docker Compose 설정 (선택)
  - 파일: `docker-compose.yml`
  - 상세: FastAPI + PostgreSQL + React(Nginx)

- [ ] **Task 7.5**: 시드 데이터 생성
  - 파일: `backend/src/infrastructure/database/seed.py`
  - 상세:
    - 관리자 계정
    - 카테고리별 샘플 아티스트
    - 샘플 공연 정보

- [ ] **Task 7.6**: 반응형 최종 검증
  - 모바일/태블릿/데스크톱 크기별 검증
  - 메뉴 네비게이션 플로우 확인
  - 이미지 최적화 확인

**🔵 REFACTOR: 최종 정리**
- [ ] **Task 7.7**: 최종 코드 정리
  - 체크리스트:
    - [ ] 불필요한 console.log/print 제거
    - [ ] 에러 핸들링 최종 점검
    - [ ] 보안 취약점 점검 (OWASP Top 10)
    - [ ] 성능 최적화 (쿼리, 번들 크기)

#### Quality Gate ✋ (최종)

**전체 시스템 검증**:
- [ ] 백엔드 모든 테스트 통과
- [ ] 프론트엔드 모든 테스트 통과
- [ ] 프론트-백 연동 정상 작동
- [ ] 반응형 디자인 검증 완료

**검증 명령어**:
```bash
# 백엔드
cd backend
pytest -v --cov=src --cov-report=html --cov-report=term-missing
ruff check src tests && black --check src tests && mypy src
pip-audit

# 프론트엔드
cd frontend
npm test && npm run build && npm run lint
npm audit
```

---

## ⚠️ 위험 평가

| 위험 | 확률 | 영향 | 완화 전략 |
|------|------|------|-----------|
| **클린 아키텍처 초기 복잡도** | 중간 | 낮음 | 단순한 구조부터 시작, 점진적 리팩토링 |
| **이메일 인증 구현 복잡성** | 중간 | 중간 | 개발 환경에서는 콘솔 출력으로 대체, SMTP 테스트 서버 사용 |
| **JWT 보안 이슈** | 중간 | 높음 | 짧은 토큰 만료, Refresh token, HTTPS 강제 |
| **프론트-백엔드 통합 문제** | 중간 | 중간 | CORS 설정, OpenAPI 스펙 활용, 통합 테스트 |
| **반응형 UI 크로스 브라우저 이슈** | 낮음 | 중간 | Tailwind CSS 활용, 주요 브라우저 테스트 |
| **이미지 업로드 성능** | 낮음 | 낮음 | 파일 크기 제한, 이미지 최적화 |
| **DB 마이그레이션 실패** | 낮음 | 높음 | 마이그레이션 전 백업, downgrade 테스트 |

---

## 🔄 롤백 전략

### Phase 1 실패 시
- Git 커밋 전 상태로 복원
- `alembic downgrade base`

### Phase 2 실패 시
- Phase 1 완료 상태로 복원
- 인증 관련 파일 제거

### Phase 3 실패 시
- Phase 2 완료 상태로 복원
- 아티스트 모듈 파일 제거
- artists 테이블 마이그레이션 롤백

### Phase 4 실패 시
- Phase 3 완료 상태로 복원
- 공연/문의 모듈 파일 제거

### Phase 5 실패 시
- Phase 4 완료 상태로 복원
- 관리자 API 파일 제거

### Phase 6 실패 시
- Phase 5 완료 상태로 복원 (백엔드 영향 없음)
- frontend/ 초기 상태로 복원

### Phase 7 실패 시
- Phase 6 완료 상태로 복원
- 통합 설정 파일만 원복

---

## 📊 진행 상황 추적

### 완료 상태
- **Phase 1**: ✅ 100%
- **Phase 2**: ✅ 100%
- **Phase 3**: ⏳ 0%
- **Phase 4**: ⏳ 0%
- **Phase 5**: ⏳ 0%
- **Phase 6**: ⏳ 0%
- **Phase 7**: ⏳ 0%

**전체 진행률**: 29% 완료 (2/7 Phase)

### 시간 추적
| Phase | 예상 시간 | 실제 시간 | 차이 |
|-------|-----------|-----------|------|
| Phase 1: 기반 구조 | 3-4 시간 | - | - |
| Phase 2: 인증 | 3-4 시간 | - | - |
| Phase 3: 섭외대행 | 3-4 시간 | - | - |
| Phase 4: 공연/문의 | 2-3 시간 | - | - |
| Phase 5: 관리자 | 2-3 시간 | - | - |
| Phase 6: 프론트엔드 | 4-5 시간 | - | - |
| Phase 7: 통합 | 2-3 시간 | - | - |
| **총계** | **19-26 시간** | **-** | **-** |

---

## 📝 노트 & 학습 내용

### 구현 노트
- FastAPI 기반 클린 아키텍처 적용
- 이메일 인증은 개발 환경에서 콘솔 출력, 프로덕션에서 SMTP 사용
- Tailwind CSS로 반응형 구현 (모바일 우선)
- 섭외대행 카테고리: 대중가수/댄서/뮤지션/연주자/오케스트라
- passlib 대신 bcrypt 직접 사용 (호환성 문제 해결)
- SQLAlchemy 모델에서 PostgreSQL 전용 타입 대신 크로스 DB 호환 타입 사용 (UUIDType, JSON, String)
- pytest-asyncio asyncio_mode = "auto" 설정 필수

### 발견한 블로커
- passlib + bcrypt 호환성 이슈 → bcrypt 직접 사용으로 해결
- PostgreSQL ARRAY/UUID/Enum 타입이 SQLite 테스트 DB에서 작동 안 함 → 커스텀 TypeDecorator로 해결
- Pydantic 유효성 검사가 422를 반환하여 Use Case의 400 에러와 충돌 → 스키마에서 validator 제거

### 향후 개선 사항
- Custom exceptions 정의하여 ValueError 대체
- Refresh token 구현
- 비밀번호 정책 상수화
- SMTP 프로덕션 이메일 발송 구현

---

## 📚 참고 자료

### 문서
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [React 공식 문서](https://react.dev/)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)
- [TanStack Query 문서](https://tanstack.com/query/latest)

---

## ✅ 최종 체크리스트

**계획을 완료로 표시하기 전**:
- [ ] 모든 Phase가 품질 게이트를 통과하며 완료됨
- [ ] 전체 통합 테스트 수행됨
- [ ] 메뉴 구조 검증: HOME/주요공연/섭외대행/문의하기
- [ ] 섭외대행 하위 메뉴: 대중가수/댄서/뮤지션/연주자/오케스트라
- [ ] 이메일 기반 회원가입 + 이메일 인증 작동
- [ ] 관리자 페이지에서 섭외대행 정보 추가/수정 가능
- [ ] 반응형 UI (모바일/태블릿/데스크톱)
- [ ] 보안 검토 완료됨
- [ ] 계획 문서 보관

---

**계획 상태**: 🔄 진행 중
**다음 액션**: Phase 3 시작 - 섭외대행 아티스트 관리 (카테고리별 CRUD)
**블로커**: 없음
