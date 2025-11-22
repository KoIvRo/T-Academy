from pathlib import Path

from exceptions import OutputError

from .adoc_exporter import ADOCExporter
from .json_exporter import JSONExporter
from .md_exporter import MDExporter


def handler(file: str, form: str, report: dict) -> None:
    """Функция для определение формата вывода."""
    if Path(file).exists():
        raise OutputError(OutputError.EXIST_MSG)

    Path(file).parent.mkdir(parents=True, exist_ok=True)

    if form.lower() == "json" and file[-4:] == "json":
        JSONExporter.export(file, report)
    elif form.lower() == "md" and file[-2:] == "md":
        MDExporter.export(file, report)
    elif form.lower() == "adoc" and file[-4:] == "adoc":
        ADOCExporter.export(file, report)
    else:
        raise OutputError(OutputError.INVALID_FORMAT_MSG)
