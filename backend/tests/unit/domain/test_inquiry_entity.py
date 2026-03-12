"""Inquiry 엔티티 유닛 테스트 (RED Phase)"""

from datetime import datetime
from uuid import uuid4

import pytest
from src.domain.entities.inquiry import Inquiry, InquiryStatus


class TestInquiryStatus:
    def test_pending_status(self):
        assert InquiryStatus.PENDING == "pending"

    def test_replied_status(self):
        assert InquiryStatus.REPLIED == "replied"

    def test_closed_status(self):
        assert InquiryStatus.CLOSED == "closed"


class TestInquiryEntity:
    def test_create_inquiry_with_valid_data(self):
        inquiry = Inquiry(
            id=uuid4(),
            name="김철수",
            email="kim@example.com",
            phone="010-1234-5678",
            subject="섭외 문의",
            message="결혼식 축가를 부탁드립니다.",
            status=InquiryStatus.PENDING,
            admin_reply=None,
            created_at=datetime.now(),
        )
        assert inquiry.name == "김철수"
        assert inquiry.email == "kim@example.com"
        assert inquiry.status == InquiryStatus.PENDING
        assert inquiry.admin_reply is None

    def test_inquiry_without_phone(self):
        inquiry = Inquiry(
            id=uuid4(),
            name="이영희",
            email="lee@example.com",
            phone=None,
            subject="공연 문의",
            message="공연 일정을 알고 싶습니다.",
            status=InquiryStatus.PENDING,
            admin_reply=None,
            created_at=datetime.now(),
        )
        assert inquiry.phone is None

    def test_inquiry_reply(self):
        inquiry = Inquiry(
            id=uuid4(),
            name="박민수",
            email="park@example.com",
            phone="010-9999-8888",
            subject="가격 문의",
            message="섭외 비용은 얼마인가요?",
            status=InquiryStatus.PENDING,
            admin_reply=None,
            created_at=datetime.now(),
        )
        inquiry.reply("섭외 비용은 상담을 통해 안내드리고 있습니다.")
        assert inquiry.status == InquiryStatus.REPLIED
        assert inquiry.admin_reply == "섭외 비용은 상담을 통해 안내드리고 있습니다."

    def test_inquiry_close(self):
        inquiry = Inquiry(
            id=uuid4(),
            name="최지은",
            email="choi@example.com",
            phone=None,
            subject="기타 문의",
            message="기타 문의 내용",
            status=InquiryStatus.REPLIED,
            admin_reply="답변 완료",
            created_at=datetime.now(),
        )
        inquiry.close()
        assert inquiry.status == InquiryStatus.CLOSED

    def test_inquiry_name_required(self):
        with pytest.raises(ValueError, match="이름"):
            Inquiry(
                id=uuid4(),
                name="",
                email="test@example.com",
                phone=None,
                subject="제목",
                message="내용",
                status=InquiryStatus.PENDING,
                admin_reply=None,
                created_at=datetime.now(),
            )

    def test_inquiry_subject_required(self):
        with pytest.raises(ValueError, match="제목"):
            Inquiry(
                id=uuid4(),
                name="홍길동",
                email="test@example.com",
                phone=None,
                subject="",
                message="내용",
                status=InquiryStatus.PENDING,
                admin_reply=None,
                created_at=datetime.now(),
            )

    def test_inquiry_message_required(self):
        with pytest.raises(ValueError, match="내용"):
            Inquiry(
                id=uuid4(),
                name="홍길동",
                email="test@example.com",
                phone=None,
                subject="제목",
                message="",
                status=InquiryStatus.PENDING,
                admin_reply=None,
                created_at=datetime.now(),
            )
