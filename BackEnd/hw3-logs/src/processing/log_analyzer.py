from datetime import datetime

from exceptions import DateError

from .log_data import LogStatistics
from .log_entry import Log
from .reader import read_logs


class LogAnalyzer:
    """Класс для сбора и анализа логов."""

    def __init__(
        self, path: str, date_from: str | None = None, date_to: str | None = None
    ) -> None:
        self.data = LogStatistics()

        self.path = path

        self.date_from: datetime = self._validate_date(date_from)
        self.date_to: datetime = self._validate_date(date_to)

        if self.date_from and self.date_to:
            self._validate_input_date(self.date_from, self.date_to)

    def analyze_logs(self) -> LogStatistics:
        """Построчно берем логи из генератора."""
        for line in read_logs(self.path):
            log = Log.parse(line)
            if not log or not self._check_date(log.timestamp):
                continue
            self.data.update(log)
        return self.data

    def _check_date(self, timestamp: datetime) -> bool:
        """Время лога в заданном пользователем промежутке."""
        return not (self.date_from and self.date_from > timestamp) or (
            self.date_to and self.date_to < timestamp
        )

    def _validate_date(self, date: str | None) -> datetime:
        """Перевод даты из iso в datetime."""
        if not date:
            return None

        try:
            return datetime.fromisoformat(date)
        except ValueError as err:
            raise DateError(DateError.INVALID_FORMAT_MSG) from err

    def _validate_input_date(self, date_from: datetime, date_to: datetime) -> None:
        """Валидация введенной даты."""
        if date_from > date_to:
            raise DateError(DateError.FROM_TO_MSG)
