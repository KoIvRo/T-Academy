class LogAnalyzeError(Exception):
    """Общий класс ислючений для программы."""


class UnexpectedError(LogAnalyzeError):
    """Неожиданное поведение программы."""

    exit_code = 1


class UsageError(LogAnalyzeError):
    """Неправильное исползование пользователем."""

    exit_code = 2


class NotFoundError(UsageError):
    """Не найден запршиваемый ресурс."""

    NOT_FOUND_PATH_MSG = "Невозможно найти информацию по указанному пути"


class InvalidFormatError(UsageError):
    """Неверный формат файла."""

    INVALID_FORMAT_MSG = "Неподходящий формат\nИспользуйте .log или .txt"


class DateError(UsageError):
    """Ошибка в указанных датах."""

    FROM_TO_MSG = "Начальная дата больше конечной"
    INVALID_FORMAT_MSG = "Неверный формат даты"


class NetworkError(UsageError):
    """Ошибки сети."""

    NET_MSG = "Ошибка сети"


class OutputError(UsageError):
    """Ошибки связанные с выводом."""

    EXIST_MSG = "Файл уже существует"
    INVALID_FORMAT_MSG = "Не поддерживаемый формат вывода"
