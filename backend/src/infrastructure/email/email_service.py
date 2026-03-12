"""이메일 발송 서비스"""

import logging

from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    async def send_verification_email(self, to_email: str, verification_token: str) -> None:
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"

        if settings.DEBUG:
            logger.info(f"[DEV] 인증 이메일 발송: {to_email}")
            logger.info(f"[DEV] 인증 링크: {verification_url}")
            print(f"\n{'='*60}")
            print("  인증 이메일 (개발 모드)")
            print(f"  수신자: {to_email}")
            print(f"  인증 링크: {verification_url}")
            print(f"{'='*60}\n")
            return

        # 프로덕션 SMTP 발송 (Phase 7에서 구현)
        logger.info(f"인증 이메일 발송: {to_email}")
