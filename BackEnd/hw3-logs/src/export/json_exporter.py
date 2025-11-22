import json
from pathlib import Path

from .exporter import Exporter


class JSONExporter(Exporter):
    """Вывод в формате json."""

    @staticmethod
    def export(file: str, report: dict) -> None:
        """Запись в файл в формате json."""
        with Path(file).open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
