from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError

from exceptions import NotFoundError
from processing.reader import FileSource, GlobSource, NetworkError, URLSource, read_logs


class TestLogReader:
    """Тестирование класса LogReader."""

    def test_exist_file(self) -> None:
        """1 - На вход передан несуществующий локальный файл."""
        with pytest.raises(NotFoundError):
            list(read_logs("unknown.log"))

    def test_validate_file(self) -> None:
        """3 - На вход передан файл в неподдерживаемом формате."""
        assert not FileSource.validate_file("unknown.jpg")

    def test_path(self) -> None:
        """Получение названия файла."""
        assert FileSource.validate_path("./test/test.txt") == " test.txt"

    def test_read_logs_file_source(self) -> None:
        """Проверка определения типа источника."""
        with patch("processing.reader.URLSource.read_logs") as mock_url:
            mock_url.return_value = iter(["log line"])
            read_logs("https://example.com/logs")
            mock_url.assert_called_once()

        with (
            patch("processing.reader.FileSource.read_logs") as mock_file,
            patch("processing.reader.Path.exists", return_value=True),
        ):
            mock_file.return_value = iter(["log line"])
            read_logs("/var/log/access.log")
            mock_file.assert_called_once()

        with patch("processing.reader.GlobSource.read_logs") as mock_glob:
            mock_glob.return_value = iter(["log line"])
            read_logs("*.log")
            mock_glob.assert_called_once()

    def test_valid_local(self) -> None:
        """11 - На вход передан валидный локальный log-файл."""
        with patch("processing.reader.Path.exists", return_value=True):
            FileSource.validate_file("exists.txt")

    @patch("processing.reader.requests.get")
    def test_valid_remote_log_file(self, mock_get: MagicMock) -> None:
        """12 - На вход передан валидный удаленный log-файл."""
        mock_response = MagicMock()
        mock_response.text = (
            '127.0.0.1 - - [01/Jan/2023:00:00:00 +0000] "GET / HTTP/1.1" 200 123'
        )
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = list(URLSource.read_logs("https://example.com/access.log"))
        assert len(result) == 1


class TestGlobSource:
    """Тесты для чтения из glob."""

    def test_glob_validation(self) -> None:
        """Проверка glob валидации."""
        assert GlobSource.glob_validation("*.log") is True
        assert GlobSource.glob_validation("file.log") is False

    def test_find_glob_files(self) -> None:
        """Проверка поиска файлов через glob."""
        with (
            patch("processing.reader.Path") as mockpath,
            patch("processing.reader.LogSource.validate_file", return_value=True),
        ):
            mock_path = MagicMock()
            mock_path.glob.return_value = [Path("file1.log")]
            mockpath.return_value = mock_path

            files = GlobSource._find_glob_files("*.log")
            assert files == ["file1.log"]


class TestURLSource:
    """Тесты для чтения из интернета."""

    @patch("processing.reader.requests.get")
    def test_url_source_success(self, mock_get: MagicMock) -> None:
        """Проверка успешного чтения из URL."""
        mock_response = MagicMock()
        mock_response.text = "line1\nline2"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        logs = list(URLSource.read_logs("https://example.com/logs"))
        assert "line1" in logs[0]

    @patch("processing.reader.requests.get")
    def test_exist_url_with_404(self, mock_get: MagicMock) -> None:
        """2 - На вход передан несуществующий удаленный файл (404)."""
        mock_get.side_effect = HTTPError("404 Client Error: Not Found for url")

        with pytest.raises(NetworkError):
            list(URLSource.read_logs("https://example.com/404.log"))
