import math

from logger_config import logger
from models import Color, Point


class Histogram:
    """Класс сбора гистораммы для определения цвета."""

    def __init__(
        self,
        width: int = 1920,
        height: int = 1080,
        gamma: float = 2.2,
        symmetry_level: int = 1,
    ) -> None:
        self.width = width
        self.height = height
        self.gamma = gamma
        self.data = {}
        self.symmetry_level = symmetry_level

    def add_point(self, point: Point, color: Color) -> None:
        """Добавление точки в гистограмму."""
        try:
            if self.symmetry_level <= 1:
                self._add_single_point(point, color)
            else:
                self._add_multi_points(point, color)
        except (KeyError, ValueError, TypeError) as e:
            logger.critical(e)

    def _rotate_point(self, point: Point, angle: float) -> Point:
        """Поворачивает точку на заданный угол вокруг центра."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        x_new = point.x * cos_a - point.y * sin_a
        y_new = point.x * sin_a + point.y * cos_a

        return Point(x_new, y_new)

    def _add_single_point(self, point: Point, color: Color) -> None:
        """Добавление точки в гистограмму."""
        # Координата в фрактале от -2 до 2
        # 4 ширина диапазона (от -2 до 2)
        x = int((point.x + 2) * self.width / 4)
        y = int((point.y + 2) * self.height / 4)

        if 0 <= x < self.width and 0 <= y < self.height:
            key = (x, y)

            if key not in self.data:
                self.data[key] = {"count": 1, "color": (color.r, color.g, color.b)}
            else:
                # Увеличиваем счетчик попаданий в пиксель
                self.data[key]["count"] += 1
                # Обновляем цвет
                old_color = self.data[key]["color"]
                self.data[key]["color"] = (
                    old_color[0] + color.r,
                    old_color[1] + color.g,
                    old_color[2] + color.b,
                )

    def _add_multi_points(self, point: Point, color: Color) -> None:
        angle_step = 2 * math.pi / self.symmetry_level

        # Зеркалим точку symmetry_level
        for rotation in range(self.symmetry_level):
            angle = rotation * angle_step
            rotated_point = self._rotate_point(point, angle)
            self._add_single_point(rotated_point, color)
