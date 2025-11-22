from abc import ABC, abstractmethod
from typing import ClassVar


class Exporter(ABC):
    """Абстрактный класс для вывода в разных форматах."""

    STATUS_NAMES: ClassVar = {
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        206: "Partial Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }

    @abstractmethod
    def export(self, file: str, report: dict) -> None:
        """Обязательный метод, вывод в файл."""

    @staticmethod
    def get_general_info(report: dict) -> tuple:
        """Подготовка столбцов с общей информации."""
        left_column = [
            "Метрика",
            "Количество запросов",
            "Средний размер ответа(b)",
            "95p размер ответа(b)",
            "Максимальный размер овтета(b)",
        ]

        right_column = [
            "Значение",
            f"{report['totalRequestsCount']}",
            f"{report['responseSizeInByte']['average']}",
            f"{report['responseSizeInByte']['max']}",
            f"{report['responseSizeInByte']['p95']}",
        ]

        return left_column, right_column

    @staticmethod
    def get_resources_info(resources: list) -> tuple:
        """Подготовка столбцов по ресурсам."""
        left_column = ["Ресурс"]
        right_column = ["Количество"]

        for resource in resources:
            left_column.append(resource["resource"])
            right_column.append(str(resource["totalRequestsCount"]))

        return left_column, right_column

    @staticmethod
    def get_response_code_info(codes: list) -> tuple:
        """Подготовка столбцов по кодам ответов."""
        left_column = ["Код"]
        middle_column = ["Имя"]
        right_column = ["Количество"]

        for code in sorted(codes, key=lambda code: code["code"]):
            left_column.append(str(code["code"]))
            middle_column.append(Exporter.STATUS_NAMES.get(code["code"], "Unknown"))
            right_column.append(str(code["totalResponsesCount"]))

        return left_column, middle_column, right_column

    @staticmethod
    def get_date_info(dates: list) -> tuple:
        """Подготовка столбцов по датам."""
        first_column = ["Дата"]
        second_column = ["День недели"]
        third_column = ["Количество"]
        fourth_column = ["% запросов"]

        for date in dates:
            first_column.append(date["date"])
            second_column.append(date["weekday"])
            third_column.append(str(date["totalRequestsCount"]))
            fourth_column.append(str(date["totalRequestsPercentage"]))

        return first_column, second_column, third_column, fourth_column

    @staticmethod
    def get_week_info(days: list) -> tuple:
        """Подготовка столбцов по дням недели."""
        left_column = ["День"]
        right_column = ["% запросов"]

        for day in days:
            left_column.append(day["day"])
            right_column.append(str(day["totalRequestsPercentage"]))

        return left_column, right_column

    @staticmethod
    def get_protocols_info(protocols: list) -> tuple:
        """Подготовка столбца по протоколам."""
        column = ["Протоколы"]

        column.extend(sorted(protocols.copy()))

        return (column,)  # Обязательно вернуть кортеж для распаковки в _creat_table
