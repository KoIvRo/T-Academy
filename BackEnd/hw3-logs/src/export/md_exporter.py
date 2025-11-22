from pathlib import Path

from .exporter import Exporter


class MDExporter(Exporter):
    """Вывод в формате md."""

    @staticmethod
    def export(file: str, report: dict) -> None:
        """Запись в файл в формате md."""
        md_report = MDExporter._report_to_md(report)
        with Path(file).open("w", encoding="utf-8") as f:
            f.write(md_report)

    @staticmethod
    def _report_to_md(report: dict) -> str:
        """Конвертация report в читаемый формат."""
        md_lines = []

        md_lines.append("#### Общая информация")
        md_lines.append("")
        md_lines.extend(MDExporter._create_table(Exporter.get_general_info(report)))
        md_lines.append("")

        md_lines.append("#### Запрашиваемые ресурсы")
        md_lines.append("")
        md_lines.extend(
            MDExporter._create_table(Exporter.get_resources_info(report["resources"]))
        )
        md_lines.append("")

        md_lines.append("#### Коды ответа")
        md_lines.append("")
        md_lines.extend(
            MDExporter._create_table(
                Exporter.get_response_code_info(report["responseCodes"])
            )
        )
        md_lines.append("")

        md_lines.append("#### Статистика по дням")
        md_lines.append("")
        md_lines.extend(
            MDExporter._create_table(Exporter.get_date_info(report["requestsPerDate"]))
        )
        md_lines.append("")

        md_lines.append("#### Статистика по дням недели")
        md_lines.append("")
        md_lines.extend(
            MDExporter._create_table(Exporter.get_week_info(report["requestsPerDay"]))
        )
        md_lines.append("")

        md_lines.append("#### Протоколы")
        md_lines.append("")
        md_lines.extend(
            MDExporter._create_table(
                Exporter.get_protocols_info(report["uniqueProtocols"])
            )
        )
        md_lines.append("")

        return "\n".join(md_lines)

    @staticmethod
    def _create_table(*columns: tuple[list]) -> list:
        """Общая функция для отрисовки таблиц по заданным колоннам."""
        table = []
        columns = columns[0]  # Распаковываем пришедшие колонки

        general_line = "|"

        for column_number in range(len(columns)):
            general_line += str(
                " "
                + columns[column_number][0]
                + (
                    " "
                    * (
                        MDExporter._get_max_width(columns[column_number])
                        - len(columns[column_number][0])
                    )
                )
                + " |"
            )

        separator_line = "|"
        for column_number in range(len(columns)):
            separator_line += str(
                ":" + "-" * (MDExporter._get_max_width(columns[column_number])) + ":|"
            )

        table.append(general_line)
        table.append(separator_line)

        for line_number in range(1, len(columns[0])):  # Не добавляем название столбца
            line = "|"
            for column_number in range(len(columns)):
                line += str(
                    " "
                    + columns[column_number][line_number]
                    + (
                        " "
                        * (
                            MDExporter._get_max_width(columns[column_number])
                            - len(columns[column_number][line_number])
                        )
                    )
                    + " |"
                )
            table.append(line)

        return table

    @staticmethod
    def _get_max_width(column: list) -> int:
        """Узнает сколько символов ширина столбца."""
        return max([len(text) for text in column])
