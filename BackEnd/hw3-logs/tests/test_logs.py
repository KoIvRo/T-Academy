from datetime import UTC, datetime

import pytest

from exceptions import DateError
from processing.log_analyzer import LogAnalyzer
from processing.log_data import LogStatistics
from processing.log_entry import Log


class TestLogAnalyzer:
    """Тестирование класса LogAnalyzer."""

    def test_date_validate(self) -> None:
        """4 - Невалидные параметры --from / --to: 2025.01.01 10:30", today."""
        with pytest.raises(DateError):
            LogAnalyzer("path", "2025-09-27T18:00:00.000", "today")

    def test_date_value(self) -> None:
        """10 --from больше, чем значение параметра --to."""
        with pytest.raises(DateError):
            LogAnalyzer("path", "2025-09-27T18:00:00.000", "2020-09-27T18:00:00.000")

    def test_timestamp(self) -> None:
        """13 - отфильтровать по --from и --to."""
        analyzer = LogAnalyzer(
            "path", "2025-09-27T18:00:00.000", "2026-09-27T18:00:00.000"
        )
        date_in = datetime.fromisoformat("2025-10-27T18:00:00.000")
        date_not = datetime.fromisoformat("2024-10-27T18:00:00.000")
        assert analyzer._check_date(date_in)
        assert not analyzer._check_date(date_not)


class TestLog:
    """Тестирование класса Log."""

    def test_parse_invalid(self) -> None:
        """14 - Локальный log-файл, часть строк в котором не подходит под формат."""
        log_invalid = Log.parse("123")
        assert not log_invalid

    def test_parse_valid(self) -> None:
        """Парсинг валидной строки."""
        log_valid = Log.parse(
            "93.180.71.3 - - [17/May/2015:08:05:32 +0000] \
            'GET /downloads/product_1 HTTP/1.1' 304 0 \
            '-' 'Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)'"
        )
        assert log_valid


class TestLogStatistics:
    """Тестирование класса LogStatistics."""

    def test_statistics_calculation_local_file(self) -> None:
        """15 - Расчет статистики на основании локального log-файла."""
        test_logs = [
            Log(
                timestamp=datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC),
                method="GET",
                resource="/index.html",
                protocol="HTTP/1.1",
                status_code=200,
                response_size=1024,
                file="access.log",
            ),
            Log(
                timestamp=datetime(2023, 1, 1, 10, 1, 0, tzinfo=UTC),
                method="POST",
                resource="/api/data",
                protocol="HTTP/1.1",
                status_code=201,
                response_size=2048,
                file="access.log",
            ),
            Log(
                timestamp=datetime(2023, 1, 2, 11, 0, 0, tzinfo=UTC),
                method="GET",
                resource="/index.html",
                protocol="HTTP/1.1",
                status_code=200,
                response_size=512,
                file="access.log",
            ),
        ]

        statistics = LogStatistics()
        for log in test_logs:
            statistics.update(log)

        report = statistics.report()

        total_requests_count = 3
        assert report["totalRequestsCount"] == total_requests_count
        assert report["files"] == ["access.log"]
        assert "HTTP/1.1" in report["uniqueProtocols"]

        max_response = 2048
        avg_response = round((1024 + 2048 + 512) / 3, 2)
        assert report["responseSizeInByte"]["max"] == max_response
        assert report["responseSizeInByte"]["average"] == avg_response

        response_codes = {
            r["code"]: r["totalResponsesCount"] for r in report["responseCodes"]
        }
        code_200 = 2
        code_201 = 1
        assert response_codes[200] == code_200
        assert response_codes[201] == code_201

    def test_report(self) -> None:
        """Проверка отчета с данными."""
        statistics = LogStatistics()

        log = Log(
            timestamp=datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC),
            method="GET",
            resource="/test",
            protocol="HTTP/1.1",
            status_code=200,
            response_size=1000,
            file="test.log",
        )
        statistics.update(log)

        report = statistics.report()

        total_count = 1
        max_response = 1000
        assert report["totalRequestsCount"] == total_count
        assert report["files"] == ["test.log"]
        assert report["responseSizeInByte"]["max"] == max_response
        assert report["uniqueProtocols"] == ["HTTP/1.1"]

        code_ind_0 = 200
        code_200_count = 1
        assert report["responseCodes"][0]["code"] == code_ind_0
        assert report["responseCodes"][0]["totalResponsesCount"] == code_200_count
