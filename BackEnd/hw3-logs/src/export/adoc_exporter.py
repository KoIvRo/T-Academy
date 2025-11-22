from pathlib import Path

from .exporter import Exporter


class ADOCExporter(Exporter):
    """Вывод в формате AsciiDoc."""

    @staticmethod
    def export(file: str, report: dict) -> None:
        """Запись в файл в формате AsciiDoc."""
        adoc_report = ADOCExporter._report_to_adoc(report)
        with Path(file).open("w", encoding="utf-8") as f:
            f.write(adoc_report)

    @staticmethod
    def _report_to_adoc(report: dict) -> str:
        adoc_lines = []

        sections = [
            ("Общая информация", Exporter.get_general_info(report)),
            (
                "Запрашиваемые ресурсы",
                Exporter.get_resources_info(report["resources"]),
            ),
            ("Коды ответа", Exporter.get_response_code_info(report["responseCodes"])),
            ("Статистика по датам", Exporter.get_date_info(report["requestsPerDate"])),
            (
                "Статистика по дням недели",
                Exporter.get_week_info(report["requestsPerDay"]),
            ),
            (
                "Используемые протоколы",
                Exporter.get_protocols_info(report["uniqueProtocols"]),
            ),
        ]

        for title, data in sections:
            adoc_lines.append(f"== {title}")
            adoc_lines.append("")
            adoc_lines.extend(ADOCExporter._create_table(data))
            adoc_lines.append("")

        return "\n".join(adoc_lines)

    @staticmethod
    def _create_table(*columns: tuple[list]) -> list:
        table_lines = []
        columns = columns[0]

        table_lines.append(
            '[cols="' + ",".join("1" * len(columns)) + '", options="header"]'
        )
        table_lines.append("|===")

        header_line = "|"
        for i in range(len(columns)):
            header_line += f" {columns[i][0]} |"
        table_lines.append(header_line)

        for row_num in range(1, len(columns[0])):
            data_line = "|"
            for i in range(len(columns)):
                data_line += f" {columns[i][row_num]} |"
            table_lines.append(data_line)

        table_lines.append("|===")

        return table_lines
