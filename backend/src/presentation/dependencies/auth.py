"""인증 의존성 (미들웨어)"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.infrastructure.security.jwt_handler import JWTHandler

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)
jwt_handler = JWTHandler()


async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        payload = jwt_handler.verify_token(credentials.credentials)
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다.",
        )


async def get_optional_user_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
) -> Optional[dict]:
    """비로그인 허용 엔드포인트용 (견적 문의 등)"""
    if not credentials:
        return None
    try:
        return jwt_handler.verify_token(credentials.credentials)
    except ValueError:
        return None


async def require_admin(payload: dict = Depends(get_current_user_token)) -> dict:
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다.",
        )
    return payload
