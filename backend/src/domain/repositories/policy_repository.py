"""Policy Repository 인터페이스"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from src.domain.entities.policy import Policy, PolicyType


class IPolicyRepository(ABC):
    @abstractmethod
    async def find_versions(self, policy_type: PolicyType) -> list[date]:
        """해당 정책의 시행일 목록 (최신순)"""
        ...

    @abstractmethod
    async def find_by_type(
        self, policy_type: PolicyType, effective_date: Optional[date] = None
    ) -> Optional[Policy]:
        """effective_date 지정 시 해당 버전, 미지정 시 최신 버전"""
        ...
