"""인증 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.application.use_cases.auth.login_user import LoginUser
from src.application.use_cases.auth.register_user import RegisterUser
from src.application.use_cases.auth.update_profile import UpdateProfile
from src.application.use_cases.auth.verify_email import VerifyEmail
from src.application.use_cases.auth.withdraw_user import WithdrawUser
from src.infrastructure.database.connection import get_db
from src.infrastructure.email.email_service import EmailService
from src.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher
from src.presentation.dependencies.auth import get_current_user_token
from src.presentation.schemas.auth import (
    LoginRequest,
    MessageResponse,
    ProfileUpdateRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _get_user_repo(db: Session = Depends(get_db)) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(db)


def _to_user_response(user, include_token: bool = False) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        phone=user.phone,
        role=user.role.value,
        is_verified=user.is_verified,
        verification_token=user.verification_token if include_token else None,
        created_at=user.created_at,
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    use_case = RegisterUser(
        user_repo=user_repo,
        password_hasher=PasswordHasher(),
        email_service=EmailService(),
    )
    try:
        user = await use_case.execute(email=request.email, password=request.password)
        # 인증 토큰은 이메일로만 전달 — API 응답에 노출하지 않음
        return _to_user_response(user, include_token=False)
    except ValueError as e:
        error_msg = str(e)
        if "이미 등록된" in error_msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


@router.get("/verify-email", response_model=MessageResponse)
async def verify_email(
    token: str = Query(...),
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    use_case = VerifyEmail(user_repo=user_repo)
    try:
        await use_case.execute(token=token)
        return MessageResponse(message="이메일 인증이 완료되었습니다.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    use_case = LoginUser(
        user_repo=user_repo,
        password_hasher=PasswordHasher(),
        jwt_handler=JWTHandler(),
    )
    try:
        result = await use_case.execute(email=request.email, password=request.password)
        return TokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=_to_user_response(result["user"]),
        )
    except ValueError as e:
        error_msg = str(e)
        if "이메일 인증" in error_msg:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_msg)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_msg)


@router.get("/me", response_model=UserResponse)
async def get_me(
    payload: dict = Depends(get_current_user_token),
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    user = await user_repo.find_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    return _to_user_response(user)


@router.put("/me", response_model=UserResponse)
async def update_me(
    request: ProfileUpdateRequest,
    payload: dict = Depends(get_current_user_token),
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    """회원정보 수정 — 이름/휴대폰/비밀번호"""
    use_case = UpdateProfile(user_repo=user_repo, password_hasher=PasswordHasher())
    try:
        user = await use_case.execute(
            user_id=payload["sub"],
            name=request.name,
            phone=request.phone,
            password=request.password,
        )
        return _to_user_response(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/me", response_model=MessageResponse)
async def withdraw_me(
    payload: dict = Depends(get_current_user_token),
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    """회원탈퇴 — 계정과 찜·장바구니 정보 삭제"""
    use_case = WithdrawUser(user_repo=user_repo)
    try:
        await use_case.execute(user_id=payload["sub"])
        return MessageResponse(message="회원탈퇴가 완료되었습니다.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(
    request: LoginRequest,
    user_repo: SqlAlchemyUserRepository = Depends(_get_user_repo),
):
    user = await user_repo.find_by_email(request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="등록되지 않은 이메일입니다.")
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 인증된 사용자입니다.")

    email_service = EmailService()
    await email_service.send_verification_email(user.email, user.verification_token)
    return MessageResponse(message="인증 이메일이 재발송되었습니다.")
