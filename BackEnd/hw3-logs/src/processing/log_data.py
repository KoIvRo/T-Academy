from collections import Counter
from datetime import UTC, datetime

import numpy as np

from .log_entry import Log


class LogStatistics:
    """Класс содержащий статистику для отчета."""

    def __init__(self) -> None:
        self.total_count_requests = 0
        self._response_size = []
        self._response_size_sum = 0
        self._max_response_size = 0

        self._files = set()
        self._protocols = set()
        self._resource = Counter()
        self._response_code = Counter()
        self._unique_days = Counter()
        self._days_of_week = Counter()

    def update(self, log: Log) -> None:
        """Функция обновления статистики."""
        self.total_count_requests += 1
        self._response_size.append(log.response_size)
        self._max_response_size = max(self._max_response_size, log.response_size)
        self._response_size_sum += log.response_size

        self._protocols.add(log.protocol)
        self._resource[log.resource] += 1
        self._response_code[log.status_code] += 1
        self._unique_days[str(log.timestamp).split()[0]] += 1
        self._days_of_week[log.day_of_week] += 1

        if log.file:
            self._files.add(log.file)

    def report(self) -> dict:
        """Подготовка отчета для вывода."""
        return {
            "files": sorted(self._files),
            "totalRequestsCount": self.total_count_requests,
            "responseSizeInByte": {
                "average": self._get_average(
                    self._response_size_sum, self.total_count_requests
                ),
                "max": self._max_response_size,
                "p95": self._get_p95(),
            },
            "resources": self._get_resource(),
            "responseCodes": self._get_response_code(),
            "requestsPerDate": self._get_requests_per_unique_day(),
            "requestsPerDay": self._get_requests_per_day(),
            "uniqueProtocols": sorted(self._protocols),
        }

    def _get_resource(self) -> list[dict]:
        """Сбор 10 ресурсов."""
        sorted_resource = sorted(self._resource)[:10]

        return [
            {"resource": resource, "totalRequestsCount": self._resource[resource]}
            for resource in sorted_resource
        ]

    def _get_response_code(self) -> list[dict]:
        """Сбор статистики встречания кодов ответа."""
        return [
            {"code": code, "totalResponsesCount": self._response_code[code]}
            for code in self._response_code
        ]

    def _get_requests_per_unique_day(self) -> list[dict]:
        """Сбор статистики по датам."""
        sorted_unique_days = sorted(self._unique_days)

        return [
            {
                "date": date,
                "weekday": datetime.strptime(date, "%Y-%m-%d")
                .replace(tzinfo=UTC)
                .strftime("%A"),
                "totalRequestsCount": self._unique_days[date],
                "totalRequestsPercentage": self._get_percentage(
                    self._unique_days[date], self.total_count_requests
                ),
            }
            for date in sorted_unique_days
        ]

    def _get_requests_per_day(self) -> list[dict]:
        """Сбор статистики по дням недели."""
        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        return [
            {
                "day": day,
                "totalRequestsCount": self._days_of_week[day],
                "totalRequestsPercentage": self._get_percentage(
                    self._days_of_week[day], self.total_count_requests
                ),
            }
            for day in days_order
            if self._days_of_week[day]
        ]

    def _get_p95(self) -> float:
        """Расчет 95 персентиля."""
        if not self._response_size:
            return 0
        return round(float(np.percentile(self._response_size, 95)), 2)

    def _get_percentage(self, size: int, total: int) -> float:
        """Функция для расчета процентов от числа.

        Аргументы:
            size - количество для расчета
            total - общее число
        Возвращение:
            Сколько size процентов от total.
        """
        if total == 0:
            return 0

        return round(size / (total / 100), 2)

    def _get_average(self, size: int, count: int) -> float:
        """Функция для расчета среднего."""
        if count == 0:
            return 0
        return round(size / count, 2)
