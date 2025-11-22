import json
from unittest.mock import MagicMock, patch

import pytest

from exceptions import OutputError
from export.output_handler import ADOCExporter, JSONExporter, MDExporter, handler


class TestHandler:
    """Класс тестирования функции hadler."""

    def test_format(self) -> None:
        """5 - Результаты запрошены в неподдерживаемом формате: txt."""
        with pytest.raises(OutputError):
            handler("unknown.txt", "txt", {1: 1})

    def test_file_format(self) -> None:
        """6 - По пути в аргументе --output указан файл с некорректным расширением."""
        with pytest.raises(OutputError):
            handler("unknown.png", "json", {1: 1})

    def test_handler(self) -> None:
        """Выбор правильного формата."""
        with patch("export.json_exporter.JSONExporter.export") as json_mock:
            handler("file.json", "json", {1: 1})
            json_mock.assert_called_once_with("file.json", {1: 1})

        with patch("export.md_exporter.MDExporter.export") as md_mock:
            handler("file.md", "md", {1: 1})
            md_mock.assert_called_once_with("file.md", {1: 1})

        with patch("export.adoc_exporter.ADOCExporter.export") as adoc_mock:
            handler("file.adoc", "adoc", {1: 1})
            adoc_mock.assert_called_once_with("file.adoc", {1: 1})


class TestOutputFormat:
    """Тесты различных форматов выходных данных."""

    def test_json_output_format(self) -> None:
        """16 - Сохранение статистики в формате JSON."""
        test_report = {
            "totalRequestsCount": 100,
            "responseSizeInByte": {"average": 500, "max": 1000, "p95": 800},
            "resources": [{"resource": "/test", "totalRequestsCount": 10}],
        }

        written_data = []

        def mock_write(data: str) -> None:
            written_data.append(data)

        mock_file = MagicMock()
        mock_file.__enter__.return_value.write = mock_write

        with patch("pathlib.Path.open", return_value=mock_file):
            JSONExporter.export("test.json", test_report)

            written_content = "".join(written_data)
            parsed_json = json.loads(written_content)

            total_requests_count = 100
            assert parsed_json["totalRequestsCount"] == total_requests_count

    def test_markdown_output_format(self) -> None:
        """17 - Сохранение статистики в формате MARKDOWN."""
        test_report = {
            "totalRequestsCount": 100,
            "responseSizeInByte": {"average": 500, "max": 1000, "p95": 800},
            "resources": [{"resource": "/test", "totalRequestsCount": 10}],
            "responseCodes": [{"code": 200, "totalResponsesCount": 90}],
            "requestsPerDate": [],
            "requestsPerDay": [],
            "uniqueProtocols": ["HTTP/1.1"],
        }

        written_data = []

        def mock_write(data: str) -> None:
            written_data.append(data)

        mock_file = MagicMock()
        mock_file.__enter__.return_value.write = mock_write

        with patch("pathlib.Path.open", return_value=mock_file):
            MDExporter.export("test.md", test_report)

            written_content = "".join(written_data)
            assert "#### Общая информация" in written_content

    def test_adoc_output_format(self) -> None:
        """18 - Сохранение статистики в формате ADOC."""
        test_report = {
            "totalRequestsCount": 100,
            "responseSizeInByte": {"average": 500, "max": 1000, "p95": 800},
            "resources": [{"resource": "/test", "totalRequestsCount": 10}],
            "responseCodes": [{"code": 200, "totalResponsesCount": 90}],
            "requestsPerDate": [],
            "requestsPerDay": [],
            "uniqueProtocols": ["HTTP/1.1"],
        }

        written_data = []

        def mock_write(data: str) -> None:
            written_data.append(data)

        mock_file = MagicMock()
        mock_file.__enter__.return_value.write = mock_write

        with patch("pathlib.Path.open", return_value=mock_file):
            ADOCExporter.export("test.adoc", test_report)

            written_content = "".join(written_data)
            assert "Общая информация" in written_content
