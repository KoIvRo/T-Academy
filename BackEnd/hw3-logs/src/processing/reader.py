from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

import requests

from exceptions import InvalidFormatError, NetworkError, NotFoundError


class LogSource(ABC):
    """Абстрактный класс для чтения логов из разных истчников."""

    @abstractmethod
    def read_logs() -> Iterator[str]:
        """Обязательный метод-генератор для возвращения строк логов."""

    @staticmethod
    def validate_file(path: str) -> bool:
        """Проверка расширения файла."""
        valid_extension: tuple[str] = (".txt", ".log")
        return Path(path).exists() and path[-4:].lower() in valid_extension

    @staticmethod
    def validate_path(path: str) -> str:
        """Функция для получения имени файла."""
        path = path.strip()

        filename = Path(path).name
        return f" {filename}"


class FileSource(LogSource):
    """Логи из файлов."""

    @staticmethod
    def read_logs(path: str) -> Iterator[str]:
        """Генерируем строки из локального файла."""
        if not LogSource.validate_file(path):
            raise InvalidFormatError(InvalidFormatError.INVALID_FORMAT_MSG)

        with Path(path).open() as log_file:
            for line in log_file:
                line_without_space = line.strip() + LogSource.validate_path(path)
                line_without_space = line_without_space.strip()
                if line_without_space:
                    yield line_without_space


class GlobSource(LogSource):
    """Класс для чтения логов из файлов с регулярными выражениями."""

    @staticmethod
    def read_logs(path: str) -> Iterator[str]:
        """Находим файлы и читаем каждый файл построчно."""
        files = GlobSource._find_glob_files(path)

        for file in files:
            # Возвращаем из генератора для локальных файлов
            yield from FileSource.read_logs(file)

    @staticmethod
    def _find_glob_files(path: str) -> list[str]:
        """Функция для поиска локальных файлов по рег выражению."""
        path_obj = Path(path)

        if path_obj.is_absolute():
            base = path_obj.anchor
            pattern = str(path_obj.relative_to(path_obj.anchor))
            return [
                str(p)
                for p in Path(base).glob(pattern)
                if LogSource.validate_file(str(p))
            ]

        return [str(p) for p in Path().glob(path) if LogSource.validate_file(str(p))]

    @staticmethod
    def glob_validation(path: str) -> bool:
        """Проверка является ли путь регулярным выражением."""
        glob_chars = {"*", "[", "]", "?"}

        return any(char in path for char in glob_chars)


class URLSource(LogSource):
    """Чтение из интернет источника."""

    @staticmethod
    def read_logs(path: str) -> Iterator[str]:
        """Читаем построчно из get ответа."""
        try:
            response = requests.get(path, timeout=3)
            # Проверяем есть ли ответ
            response.raise_for_status()

            content = response.text
            for line in content.split("\n"):
                line_without_space = line.strip() + f" {path}"
                line_without_space = line_without_space.strip()
                if line_without_space:
                    yield line_without_space

        except requests.exceptions.RequestException as err:
            raise NetworkError(NetworkError.NET_MSG) from err


def read_logs(path: str) -> Iterator[str]:
    """Определение ресурса логов и вовращение генератора."""
    if path.startswith(("https://", "http://")):
        return URLSource.read_logs(path)

    if Path(path).exists():
        return FileSource.read_logs(path)

    if GlobSource.glob_validation(path):
        return GlobSource.read_logs(path)

    raise NotFoundError(NotFoundError.NOT_FOUND_PATH_MSG)
