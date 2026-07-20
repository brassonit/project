"""이메일 발송 서비스"""

import asyncio
import logging
import os
import ssl
from email.message import EmailMessage
from email.utils import formataddr

import aiosmtplib
import certifi
import httpx

from src.domain.entities.quote import Quote
from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


def _smtp_configured() -> bool:
    return bool(settings.SMTP_HOST and settings.SMTP_HOST != "localhost" and settings.SMTP_USER and settings.SMTP_PASSWORD)


def _admin_emails() -> list[str]:
    return [e.strip() for e in settings.ADMIN_NOTIFICATION_EMAILS.split(",") if e.strip()]


def _fetch_attachment(file_url: str) -> bytes | None:
    """첨부파일 로딩 — 로컬 /uploads/는 디스크에서, 그 외(오라클 Object Storage 등)는 URL에서"""
    try:
        if file_url.startswith("/uploads/"):
            path = os.path.join(settings.UPLOAD_DIR, file_url.replace("/uploads/", "", 1))
            with open(path, "rb") as f:
                return f.read()
        if file_url.startswith("http://") or file_url.startswith("https://"):
            res = httpx.get(file_url, timeout=15)
            res.raise_for_status()
            return res.content
    except Exception as e:  # 첨부 실패는 메일 발송을 막지 않음
        logger.warning(f"첨부파일 로딩 실패: {file_url} ({e})")
    return None


class EmailService:
    async def send_verification_email(self, to_email: str, verification_token: str) -> None:
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        subject = "[브라소닛] 이메일 인증을 완료해주세요"

        text_body = (
            "브라소닛 회원가입을 환영합니다.\n\n"
            "아래 링크를 열어 이메일 인증을 완료해주세요.\n"
            f"{verification_url}\n\n"
            "본인이 요청하지 않았다면 이 메일을 무시하셔도 됩니다."
        )
        html_body = (
            '<div style="font-family:sans-serif;max-width:480px;margin:0 auto;color:#222">'
            '<h2 style="border-bottom:2px solid #000;padding-bottom:10px">이메일 인증</h2>'
            "<p>브라소닛 회원가입을 환영합니다.<br>아래 버튼을 눌러 이메일 인증을 완료해주세요.</p>"
            '<p style="text-align:center;margin:32px 0">'
            f'<a href="{verification_url}" style="display:inline-block;background:#000;color:#fff;'
            'padding:14px 28px;text-decoration:none;border-radius:4px;font-weight:bold">이메일 인증하기</a></p>'
            '<p style="color:#888;font-size:12px">버튼이 동작하지 않으면 아래 링크를 브라우저 주소창에 붙여넣어주세요.<br>'
            f'<a href="{verification_url}">{verification_url}</a></p>'
            '<p style="color:#888;font-size:12px;border-top:1px solid #ddd;padding-top:14px">'
            "brassonit — 연예인 섭외대행 · 공연기획</p></div>"
        )

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = formataddr(("브라소닛", settings.SMTP_FROM_EMAIL))
        msg["To"] = to_email
        msg.set_content(text_body)
        msg.add_alternative(html_body, subtype="html")

        if not _smtp_configured():
            logger.info(f"[DEV] 인증 이메일 (SMTP 미설정 — 콘솔 출력): {to_email}")
            print(f"\n{'='*60}")
            print("  인증 이메일 (개발 모드)")
            print(f"  수신자: {to_email}")
            print(f"  인증 링크: {verification_url}")
            print(f"{'='*60}\n", flush=True)
            return

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=settings.SMTP_USE_TLS,
                tls_context=ssl.create_default_context(cafile=certifi.where()),
            )
            logger.info(f"인증 이메일 발송 완료: {to_email}")
        except Exception as e:  # 발송 실패가 회원가입 자체를 막지 않도록
            logger.error(f"인증 이메일 발송 실패: {e}")

    async def send_quote_notification(self, quote: Quote) -> None:
        """견적(공연/아티스트) 등록 알림 — 등록 내용 + 첨부파일을 관리자 메일로 발송"""
        to_emails = _admin_emails()
        if not to_emails:
            return

        kind = "공연 견적" if quote.show_id else "섭외 견적"
        subject = f"[브라소닛] 새 {kind} 접수 — {quote.event_title}"

        event_date = quote.event_date.isoformat() if quote.event_date else (quote.event_date_text or "미정")
        artists = ", ".join(a.artist_name or a.artist_id for a in quote.artists) or "-"
        rows = [
            ("행사명", quote.event_title),
            ("담당자", f"{quote.name} ({quote.email} / {quote.phone})"),
            ("행사일", event_date),
            ("행사지역", quote.region or "-"),
            ("아티스트", artists),
        ]
        if quote.show_id:
            rows.append(("첨부 공연", quote.show_title or "-"))
        if quote.show_id and quote.show_lineup:
            rows.append(("출연진", ", ".join(quote.show_lineup)))
        rows.append(("내용", quote.content or "-"))
        text_body = f"새 {kind}이 접수되었습니다.\n\n" + "\n".join(f"{k} : {v}" for k, v in rows)
        html_rows = "".join(
            f'<tr><td style="padding:6px 12px;color:#888;white-space:nowrap;vertical-align:top">{k}</td>'
            f'<td style="padding:6px 12px;white-space:pre-wrap">{v}</td></tr>'
            for k, v in rows
        )
        html_body = (
            f'<div style="font-family:sans-serif;max-width:640px">'
            f'<h2 style="border-bottom:2px solid #000;padding-bottom:10px">새 {kind} 접수</h2>'
            f'<table style="border-collapse:collapse;font-size:14px">{html_rows}</table>'
            f'<p style="color:#888;font-size:12px">brassonit — 연예인 섭외대행 · 공연기획</p></div>'
        )

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = formataddr(("브라소닛", settings.SMTP_FROM_EMAIL))
        msg["To"] = ", ".join(to_emails)
        msg.set_content(text_body)
        msg.add_alternative(html_body, subtype="html")

        # 첨부파일 — 오라클 Object Storage(공개 URL) 또는 로컬 uploads/에서 로딩해 첨부
        for att in quote.attachments:
            data = await asyncio.to_thread(_fetch_attachment, att.file_url)
            if data is None:
                continue
            msg.add_attachment(
                data,
                maintype="application",
                subtype="octet-stream",
                filename=att.file_name,
            )

        if not _smtp_configured():
            att_names = ", ".join(a.file_name for a in quote.attachments) or "없음"
            logger.info(f"[DEV] 견적 알림 메일 (SMTP 미설정 — 콘솔 출력): {to_emails}")
            print(f"\n{'='*60}")
            print(f"  {subject}")
            print(f"  수신자: {', '.join(to_emails)}")
            for k, v in rows:
                print(f"  {k} : {v}")
            print(f"  첨부파일 : {att_names}")
            print(f"{'='*60}\n", flush=True)
            return

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=settings.SMTP_USE_TLS,
                # 시스템 CA 미탑재 환경(macOS python.org 빌드 등)에서도 TLS 검증 가능하도록 certifi 사용
                tls_context=ssl.create_default_context(cafile=certifi.where()),
            )
            logger.info(f"견적 알림 메일 발송 완료: {to_emails}")
        except Exception as e:  # 알림 실패가 견적 접수를 막지 않도록
            logger.error(f"견적 알림 메일 발송 실패: {e}")
