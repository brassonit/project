"""인증 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.application.use_cases.auth.login_user import LoginUser
from src.application.use_cases.auth.register_user import RegisterUser
from src.application.use_cases.auth.verify_email import VerifyEmail
from src.infrastructure.database.connection import get_db
from src.infrastructure.email.email_service import EmailService
from src.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher
from src.presentation.dependencies.auth import get_current_user_token
from src.presentation.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _get_user_repo(db: Session = Depends(get_db)) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(db)


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
        return UserResponse(
            id=user.id,
            email=user.email,
            role=user.role.value,
            is_verified=user.is_verified,
            created_at=user.created_at,
        )
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
        user = result["user"]
        return TokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UserResponse(
                id=user.id,
                email=user.email,
                role=user.role.value,
                is_verified=user.is_verified,
                created_at=user.created_at,
            ),
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
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role.value,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )


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
