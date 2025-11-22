import argparse
import sys

from exceptions import UnexpectedError, UsageError
from export.output_handler import handler
from logger_config import logger
from processing.log_analyzer import LogAnalyzer


def parse_args() -> argparse.Namespace:
    """Сбор аргументов при запуске."""
    parser = argparse.ArgumentParser(description="Обработка аргументов.")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Путь к одному или нескольким NGINX лог-файлам",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Путь для сохранения лабиринта", required=True
    )
    parser.add_argument(
        "-f", "--format", type=str, help="Начальная точка маршрута", required=True
    )
    parser.add_argument(
        "--from", type=str, help="Конечная точка маршрута", default=None
    )
    parser.add_argument("--to", type=str, help="Конечная точка маршрута", default=None)

    return parser.parse_args()


def main() -> None:
    """Точка входа в приложение."""
    try:
        logger.info("Запуск")
        args = parse_args()
        logger.info("Аргументы собраны")

        logger.info("Начался сбор информации из источников")
        analyzer = LogAnalyzer(
            args.path, getattr(args, "from", None), getattr(args, "to", None)
        )
        statistics = analyzer.analyze_logs()
        logger.info(f"Информация с {statistics.total_count_requests} записей собрана")

        logger.info("Подготовка отчета")
        report = statistics.report()
        logger.info(f"Готов по отчет по источникам: {report['files']}")

        logger.info("Запись в файл")
        handler(args.output, args.format, report)
        logger.info(f"Файл {args.output} в формате {args.format} с отчетом создан")
    except UsageError as e:
        print(e)
        return e.exit_code
    except (PermissionError, ValueError, TypeError, AttributeError) as e:
        print(e)
        return UnexpectedError.exit_code


if __name__ == "__main__":
    sys.exit(main())
