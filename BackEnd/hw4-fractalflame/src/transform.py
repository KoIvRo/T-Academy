import math
import random

from logger_config import logger
from models import Color, Point


class Transformations:
    """Класс с трансормациями."""

    @staticmethod
    def linear(point: Point, color: Color) -> Point:
        """Без изменений."""
        function_color = Color(0.95, 0.85, 0.1)  # Яркое золото
        return point, Transformations._new_color(function_color, color)

    @staticmethod
    def swirl(point: Point, color: Color) -> Point:
        """Закручивание вокруг центра."""
        function_color = Color(0.9, 0.3, 0.1)  # Огненно-красный
        r = math.sqrt(abs(point.x * point.x + point.y * point.y))
        return Point(
            point.x * math.sin(r * r) - point.y * math.cos(r * r),
            point.x * math.cos(r * r) + point.y * math.sin(r * r),
        ), Transformations._new_color(function_color, color)

    @staticmethod
    def horseshoe(point: Point, color: Color) -> Point:
        """Отражение как в подкове."""
        function_color = Color(0.95, 0.6, 0.1)  # Насыщенный оранжевый
        r = math.sqrt(point.x * point.x + point.y * point.y)
        if r == 0:
            return Point(0, 0)
        return Point(
            (point.x - point.y) * (point.x + point.y) / r, 2 * point.x * point.y / r
        ), Transformations._new_color(function_color, color)

    @staticmethod
    def sinusoidal(point: Point, color: Color) -> tuple:
        """Синусоидальное искажение с расширенным диапазоном."""
        function_color = Color(0.8, 0.9, 0.2)

        # РАСШИРЕННЫЙ диапазон - умножаем на коэффициент
        scale = 3.0  # увеличивает амплитуду
        # Без увеличения, очень малый диапазон значении функции
        return Point(
            math.sin(point.x) * scale, math.sin(point.y) * scale
        ), Transformations._new_color(function_color, color)

    @staticmethod
    def spherical(point: Point, color: Color) -> Point:
        """Сферическое искажение."""
        function_color = Color(0.7, 0.2, 0.1)  # Темно-красный, бордовый
        r = math.sqrt(point.x * point.x + point.y * point.y)
        if r == 0:
            return Point(0, 0), Transformations._new_color(function_color, color)
        return Point(point.x / (r * r), point.y / (r * r)), Transformations._new_color(
            function_color, color
        )

    @staticmethod
    def spiral_waves(point: Point, color: Color) -> Point:
        """Спиральные волны."""
        function_color = Color(0.95, 0.8, 0.3)  # Светлое золото

        r = math.sqrt(abs(point.x * point.x + point.y * point.y))
        theta = math.atan2(point.y, point.x)

        wave = math.sin(theta * 5) * 0.3
        new_r = r * (1 + wave)
        new_theta = theta + r * 1.5

        return Point(
            new_r * math.cos(new_theta), new_r * math.sin(new_theta)
        ), Transformations._new_color(function_color, color)

    @staticmethod
    def vortex_rings(point: Point, color: Color) -> Point:
        """Вихревые кольца."""
        function_color = Color(0.9, 0.5, 0.1)  # Яркий оранжевый

        r = math.sqrt(abs(point.x * point.x + point.y * point.y))
        theta = math.atan2(point.y, point.x)

        rings = math.sin(r * 8) * 0.2
        new_r = r * (1 + rings)

        new_theta = theta + math.log(abs(r) + 1) * 2

        return Point(
            new_r * math.cos(new_theta), new_r * math.sin(new_theta)
        ), Transformations._new_color(function_color, color)

    @staticmethod
    def get_variation(name: str) -> callable:
        """Возвращает функцию вариации по имени."""
        variations: dict = {
            "linear": Transformations.linear,
            "swirl": Transformations.swirl,
            "horseshoe": Transformations.horseshoe,
            "sinusoidal": Transformations.sinusoidal,
            "spherical": Transformations.spherical,
            "spiral_waves": Transformations.spiral_waves,
            "vortex_rings": Transformations.vortex_rings,
        }
        return variations.get(name, Transformations.linear)

    @staticmethod
    def _new_color(function_color: Color, new_color: Color) -> Color:
        return Color(
            (new_color.r + function_color.r) / 2,
            (new_color.g + function_color.g) / 2,
            (new_color.b + function_color.b) / 2,
        )


class AffineTransformer:
    """Выполняет аффинные преобразования."""

    def __init__(
        self, a: float, b: float, c: float, d: float, e: float, f: float
    ) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

        self._normalize()

    def transform(self, point: Point) -> Point:
        """Применяет аффинное преобразование к точке."""
        return Point(
            self.a * point.x + self.b * point.y + self.c,
            self.d * point.x + self.e * point.y + self.f,
        )

    def _normalize(self) -> None:
        """Нормализует аффинную матрицу так, чтобы она не разгоняла точки."""
        # Находим определитель матрицы аффинных параметров
        det = abs(self.a * self.e - self.b * self.d)

        # Аффинные параметры разгоняют значения до inf, если их det > 1
        if det > 1:
            scale = 1 / math.sqrt(det)

            self.a *= scale
            self.b *= scale
            self.c *= scale
            self.d *= scale
            self.e *= scale
            self.f *= scale

            logger.warning("Аффинные параметры были принудительно уменьшены")


class TransformationSystem:
    """Управление трансформациями."""

    def __init__(self, function_params: list, affine_params: dict) -> None:
        self.ap_transformer = AffineTransformer(**affine_params)
        # Сортируем по возрастанию
        self.function_params = sorted(function_params, key=lambda x: x["weight"])

        self.function_total_weight = sum(func["weight"] for func in function_params)

    def transform_point(self, point: Point, color: Color) -> Point:
        """Применить трнасформацию к точке."""
        try:
            point = self.ap_transformer.transform(point)

            trans = Transformations.get_variation(self._choose_random_transform())
            point, color = trans(point, color)

        except (ZeroDivisionError, ValueError, TypeError):
            return point, color
        else:
            return point, color

    def _choose_random_transform(self) -> str:
        """Выбрать вариацию трансформацию."""
        rand = random.random() * self.function_total_weight
        cur_weight = 0

        # Накапливаем вес, начиная с минимальных.
        # Когда вес стал больше рандомного значения, мы выбрали функцию
        for func in self.function_params:
            cur_weight += func["weight"]
            if cur_weight >= rand:
                return func["name"]

        return "linear"
