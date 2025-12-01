import time
from functools import wraps

from logger_config import logger


def measure_time(message: str = "Функция завершила работу.") -> callable:
    """Надостройка над декоратор для принятия сообщения."""

    def decorator(func: callable) -> callable:
        """Декоратор для замера времени."""

        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> callable:
            """Функция замера времени."""
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger.info(f"{message} Времени затрачено: {end - start:.2f}")
            return result

        return wrapper

    return decorator
