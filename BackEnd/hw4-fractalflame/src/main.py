import sys

from config import Config
from engine import FractalEngine
from image import ImageExporter
from logger_config import logger
from measure import measure_time


@measure_time("Генерация завершена.")
def main() -> None:
    """Точка входа в приложение."""
    try:
        config = Config()
        config.load_with_priority()
        logger.info("Аргументы собраны")

        engine = FractalEngine(config)
        exporter = ImageExporter(
            config.width, config.height, config.gamma, config.output_path
        )

        logger.info("Начинается генерация")
        hist = engine.generate()
        exporter.save(hist.data)
    except KeyboardInterrupt:
        logger.info("Программа прервана пользователем")
        sys.exit(130)
    except Exception as e:  # noqa: BLE001
        logger.critical(e)
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
