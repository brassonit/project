"""문의 Use Case 유닛 테스트"""

from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from src.application.use_cases.inquiry.create_inquiry import CreateInquiry
from src.application.use_cases.inquiry.delete_inquiry import DeleteInquiry
from src.application.use_cases.inquiry.list_inquiries import ListInquiries
from src.application.use_cases.inquiry.reply_inquiry import ReplyInquiry
from src.application.use_cases.inquiry.update_inquiry_status import UpdateInquiryStatus
from src.domain.entities.inquiry import Inquiry, InquiryStatus


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def sample_inquiry():
    return Inquiry(
        id=uuid4(),
        name="홍길동",
        email="hong@example.com",
        phone="010-1234-5678",
        subject="섭외 문의",
        message="가수 섭외를 요청합니다.",
        status=InquiryStatus.PENDING,
        admin_reply=None,
        created_at=datetime.now(),
    )


@pytest.fixture
def sample_inquiries():
    return [
        Inquiry(
            id=uuid4(),
            name="홍길동",
            email="hong@example.com",
            phone=None,
            subject="문의1",
            message="내용1",
            status=InquiryStatus.PENDING,
            created_at=datetime.now(),
        ),
        Inquiry(
            id=uuid4(),
            name="김철수",
            email="kim@example.com",
            phone=None,
            subject="문의2",
            message="내용2",
            status=InquiryStatus.REPLIED,
            admin_reply="답변입니다.",
            created_at=datetime.now(),
        ),
        Inquiry(
            id=uuid4(),
            name="이영희",
            email="lee@example.com",
            phone=None,
            subject="문의3",
            message="내용3",
            status=InquiryStatus.CLOSED,
            created_at=datetime.now(),
        ),
    ]


class TestCreateInquiry:
    @pytest.mark.asyncio
    async def test_create_success(self, mock_repo, sample_inquiry):
        mock_repo.save.return_value = sample_inquiry
        use_case = CreateInquiry(inquiry_repo=mock_repo)

        result = await use_case.execute(
            name="홍길동",
            email="hong@example.com",
            subject="섭외 문의",
            message="가수 섭외를 요청합니다.",
            phone="010-1234-5678",
        )

        assert result.name == "홍길동"
        assert result.status == InquiryStatus.PENDING
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_without_phone(self, mock_repo, sample_inquiry):
        mock_repo.save.return_value = sample_inquiry
        use_case = CreateInquiry(inquiry_repo=mock_repo)

        result = await use_case.execute(
            name="홍길동",
            email="hong@example.com",
            subject="문의",
            message="내용",
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_invalid_email(self, mock_repo):
        use_case = CreateInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="이메일"):
            await use_case.execute(
                name="홍길동",
                email="bad-email",
                subject="문의",
                message="내용",
            )

    @pytest.mark.asyncio
    async def test_create_empty_name_raises(self, mock_repo):
        use_case = CreateInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="이름"):
            await use_case.execute(
                name="",
                email="test@example.com",
                subject="문의",
                message="내용",
            )

    @pytest.mark.asyncio
    async def test_create_empty_subject_raises(self, mock_repo):
        use_case = CreateInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="제목"):
            await use_case.execute(
                name="홍길동",
                email="test@example.com",
                subject="",
                message="내용",
            )

    @pytest.mark.asyncio
    async def test_create_empty_message_raises(self, mock_repo):
        use_case = CreateInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="내용"):
            await use_case.execute(
                name="홍길동",
                email="test@example.com",
                subject="문의",
                message="",
            )


class TestListInquiries:
    @pytest.mark.asyncio
    async def test_list_all(self, mock_repo, sample_inquiries):
        mock_repo.find_all.return_value = sample_inquiries
        mock_repo.count_all.return_value = 3
        use_case = ListInquiries(inquiry_repo=mock_repo)

        result = await use_case.execute()
        assert result["total"] == 3
        assert len(result["inquiries"]) == 3

    @pytest.mark.asyncio
    async def test_list_by_status(self, mock_repo, sample_inquiries):
        pending = [i for i in sample_inquiries if i.status == InquiryStatus.PENDING]
        mock_repo.find_by_status.return_value = pending
        mock_repo.count_by_status.return_value = 1
        use_case = ListInquiries(inquiry_repo=mock_repo)

        result = await use_case.execute(status="pending")
        assert result["total"] == 1

    @pytest.mark.asyncio
    async def test_list_invalid_status_raises(self, mock_repo):
        use_case = ListInquiries(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="상태"):
            await use_case.execute(status="invalid")

    @pytest.mark.asyncio
    async def test_list_pagination(self, mock_repo, sample_inquiries):
        mock_repo.find_all.return_value = sample_inquiries[:2]
        mock_repo.count_all.return_value = 3
        use_case = ListInquiries(inquiry_repo=mock_repo)

        result = await use_case.execute(skip=0, limit=2)
        assert len(result["inquiries"]) == 2
        assert result["total"] == 3


class TestReplyInquiry:
    @pytest.mark.asyncio
    async def test_reply_success(self, mock_repo, sample_inquiry):
        mock_repo.find_by_id.return_value = sample_inquiry
        replied = Inquiry(
            id=sample_inquiry.id,
            name=sample_inquiry.name,
            email=sample_inquiry.email,
            phone=sample_inquiry.phone,
            subject=sample_inquiry.subject,
            message=sample_inquiry.message,
            status=InquiryStatus.REPLIED,
            admin_reply="답변입니다.",
            created_at=sample_inquiry.created_at,
        )
        mock_repo.update.return_value = replied
        use_case = ReplyInquiry(inquiry_repo=mock_repo)

        result = await use_case.execute(inquiry_id=sample_inquiry.id, reply_text="답변입니다.")
        assert result.status == InquiryStatus.REPLIED
        assert result.admin_reply == "답변입니다."

    @pytest.mark.asyncio
    async def test_reply_not_found(self, mock_repo):
        mock_repo.find_by_id.return_value = None
        use_case = ReplyInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="문의를 찾을 수 없습니다"):
            await use_case.execute(inquiry_id=uuid4(), reply_text="답변")

    @pytest.mark.asyncio
    async def test_reply_empty_text_raises(self, mock_repo, sample_inquiry):
        mock_repo.find_by_id.return_value = sample_inquiry
        use_case = ReplyInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="답변 내용"):
            await use_case.execute(inquiry_id=sample_inquiry.id, reply_text="")


class TestUpdateInquiryStatus:
    @pytest.mark.asyncio
    async def test_update_status_success(self, mock_repo, sample_inquiry):
        mock_repo.find_by_id.return_value = sample_inquiry
        closed = Inquiry(
            id=sample_inquiry.id,
            name=sample_inquiry.name,
            email=sample_inquiry.email,
            phone=sample_inquiry.phone,
            subject=sample_inquiry.subject,
            message=sample_inquiry.message,
            status=InquiryStatus.CLOSED,
            created_at=sample_inquiry.created_at,
        )
        mock_repo.update.return_value = closed
        use_case = UpdateInquiryStatus(inquiry_repo=mock_repo)

        result = await use_case.execute(inquiry_id=sample_inquiry.id, status="closed")
        assert result.status == InquiryStatus.CLOSED

    @pytest.mark.asyncio
    async def test_update_status_not_found(self, mock_repo):
        mock_repo.find_by_id.return_value = None
        use_case = UpdateInquiryStatus(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="문의를 찾을 수 없습니다"):
            await use_case.execute(inquiry_id=uuid4(), status="closed")

    @pytest.mark.asyncio
    async def test_update_invalid_status_raises(self, mock_repo, sample_inquiry):
        mock_repo.find_by_id.return_value = sample_inquiry
        use_case = UpdateInquiryStatus(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="상태"):
            await use_case.execute(inquiry_id=sample_inquiry.id, status="invalid")


class TestDeleteInquiry:
    @pytest.mark.asyncio
    async def test_delete_success(self, mock_repo, sample_inquiry):
        mock_repo.find_by_id.return_value = sample_inquiry
        use_case = DeleteInquiry(inquiry_repo=mock_repo)

        await use_case.execute(inquiry_id=sample_inquiry.id)
        mock_repo.delete.assert_called_once_with(sample_inquiry.id)

    @pytest.mark.asyncio
    async def test_delete_not_found(self, mock_repo):
        mock_repo.find_by_id.return_value = None
        use_case = DeleteInquiry(inquiry_repo=mock_repo)

        with pytest.raises(ValueError, match="문의를 찾을 수 없습니다"):
            await use_case.execute(inquiry_id=uuid4())
