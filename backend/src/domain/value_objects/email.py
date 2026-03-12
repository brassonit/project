"""이메일 Value Object"""

import re


class Email:
    _EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def __init__(self, value: str) -> None:
        normalized = value.strip().lower()
        if not normalized or not self._EMAIL_REGEX.match(normalized):
            raise ValueError("유효하지 않은 이메일 형식입니다.")
        self._value = normalized

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Email({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)
