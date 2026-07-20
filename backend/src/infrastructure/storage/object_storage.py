"""Oracle Object Storage (S3 호환 API) 저장소 서비스

OCI_* 설정이 있으면 견적 첨부파일을 버킷에 저장하고,
없으면 호출부에서 로컬 FileStorage로 폴백한다.
"""

import os
import uuid
from urllib.parse import quote

import boto3
from botocore.config import Config as BotoConfig
from fastapi import UploadFile

from src.infrastructure.config import settings


class OciObjectStorage:
    def __init__(self) -> None:
        self.namespace = settings.OCI_NAMESPACE
        self.bucket = settings.OCI_BUCKET_NAME
        self.region = settings.OCI_REGION
        # S3 호환 엔드포인트: https://{namespace}.compat.objectstorage.{region}.oraclecloud.com
        self.client = boto3.client(
            "s3",
            region_name=self.region,
            endpoint_url=f"https://{self.namespace}.compat.objectstorage.{self.region}.oraclecloud.com",
            aws_access_key_id=settings.OCI_ACCESS_KEY,
            aws_secret_access_key=settings.OCI_SECRET_KEY,
            config=BotoConfig(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
                # OCI S3 호환 API는 aws-chunked 인코딩 미지원 (boto3 1.36+ 기본값 회피)
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        )

    @staticmethod
    def is_configured() -> bool:
        return bool(
            settings.OCI_NAMESPACE
            and settings.OCI_BUCKET_NAME
            and settings.OCI_REGION
            and settings.OCI_ACCESS_KEY
            and settings.OCI_SECRET_KEY
        )

    def _object_url(self, key: str) -> str:
        """네이티브 공개 URL — https://objectstorage.{region}.oraclecloud.com/n/{ns}/b/{bucket}/o/{key}"""
        return (
            f"https://objectstorage.{self.region}.oraclecloud.com"
            f"/n/{self.namespace}/b/{self.bucket}/o/{quote(key, safe='')}"
        )

    async def save_attachment(self, file: UploadFile) -> str:
        """견적 첨부파일 업로드 — 문서/이미지/압축 확장자 허용, 객체 URL 반환"""
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in settings.ALLOWED_ATTACHMENT_EXTS:
            allowed = ", ".join(settings.ALLOWED_ATTACHMENT_EXTS)
            raise ValueError(f"허용되지 않는 파일 형식입니다. 허용: {allowed}")

        contents = await file.read()
        if len(contents) > settings.MAX_UPLOAD_SIZE:
            max_mb = settings.MAX_UPLOAD_SIZE // (1024 * 1024)
            raise ValueError(f"파일 크기가 {max_mb}MB를 초과합니다.")

        # 첨부파일 전용 경로 — 버킷 내 uploads/ 아래에 저장
        key = f"uploads/{uuid.uuid4()}{ext}"
        extra = {}
        if file.content_type:
            extra["ContentType"] = file.content_type
        if file.filename:
            # 다운로드 시 원본 파일명 유지 (RFC 5987)
            extra["ContentDisposition"] = f"attachment; filename*=UTF-8''{quote(file.filename)}"
        self.client.put_object(Bucket=self.bucket, Key=key, Body=contents, **extra)
        return self._object_url(key)
