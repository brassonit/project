"""로컬 파일 저장소 서비스"""

import os
import uuid

from fastapi import UploadFile

from src.infrastructure.config import settings


class FileStorage:
    def __init__(self) -> None:
        self.upload_dir = settings.UPLOAD_DIR
        self.max_size = settings.MAX_UPLOAD_SIZE
        self.allowed_types = settings.ALLOWED_IMAGE_TYPES
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_image(self, file: UploadFile) -> str:
        if file.content_type not in self.allowed_types:
            allowed = ", ".join(self.allowed_types)
            raise ValueError(f"허용되지 않는 파일 형식입니다. 허용: {allowed}")

        contents = await file.read()
        if len(contents) > self.max_size:
            max_mb = self.max_size // (1024 * 1024)
            raise ValueError(f"파일 크기가 {max_mb}MB를 초과합니다.")

        ext = os.path.splitext(file.filename or "image.jpg")[1] or ".jpg"
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(self.upload_dir, filename)

        with open(filepath, "wb") as f:
            f.write(contents)

        return f"/uploads/{filename}"

    async def delete_image(self, file_url: str) -> None:
        if file_url and file_url.startswith("/uploads/"):
            filename = file_url.replace("/uploads/", "")
            filepath = os.path.join(self.upload_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
