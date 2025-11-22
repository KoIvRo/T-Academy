from datetime import datetime
from typing import Optional

from exceptions import DateError
from logger_config import logger


class Log:
    """Cодержание лога."""

    def __init__(
        self,
        timestamp: datetime,
        method: str,
        resource: str,
        protocol: str,
        status_code: int,
        response_size: int,
        file: str | None = None,
    ) -> None:
        self.timestamp = timestamp
        self.method = method
        self.resource = resource
        self.protocol = protocol
        self.status_code = status_code
        self.response_size = response_size
        self.file = file

    @classmethod
    def parse(cls, line: str) -> Optional["Log"]:
        """Сбор ифнормации из строки с логом."""
        max_len_log_parts: int = 12

        try:
            parts = line.split()

            if len(parts) < max_len_log_parts:
                return None

            timestamp_str = f"{parts[3][1:]} {parts[4][:-1]}"

            method = parts[5].removeprefix('"')
            resource = parts[6]
            protocol = parts[7].removesuffix('"')

            status_code = int(parts[8])
            response_size = int(parts[9])

            file = parts[-1]

            timestamp = cls._parse_timestamp(timestamp_str)
            if not timestamp:
                logger.warning(f"СТРОКА НЕ ОБРАБОТАНА: {line}")
                return None
        except (ValueError, AttributeError, TypeError, DateError):
            logger.warning(f"СТРОКА НЕ ОБРАБОТАНА: {line}")
            return None
        else:
            return cls(
                timestamp, method, resource, protocol, status_code, response_size, file
            )

    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> datetime:
        """Перевод даты лога в формат datetime."""
        try:
            formatted = timestamp_str.replace(":", " ", 1)
            return datetime.strptime(formatted, "%d/%b/%Y %H:%M:%S %z")
        except (ValueError, AttributeError):
            return None

    @property
    def day_of_week(self) -> str:
        """Определение дня недели."""
        return self.timestamp.strftime("%A")
