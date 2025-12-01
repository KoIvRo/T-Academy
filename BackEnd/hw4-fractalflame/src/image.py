import math

from PIL import Image

from logger_config import logger
from measure import measure_time


class ImageExporter:
    """Класс для сохранения изображений."""

    def __init__(self, width: int, height: int, gamma: float, path: str) -> None:
        self.width = width
        self.height = height
        self.gamma = gamma
        self.path = path

    def save(self, hist: dict) -> None:
        """Преобразования и сохранение изображение."""
        try:
            image = self._hist_to_image(hist)
            image.save(self.path)
            logger.info(f"Изображение сохранено в файл {self.path}")
        except (PermissionError, IsADirectoryError) as e:
            logger.critical(e)

    @measure_time("Изображение создано.")
    def _hist_to_image(self, hist: dict) -> Image:
        """Создание изображения по гистограмме."""
        image = Image.new("RGB", (self.width, self.height), "black")
        pixels = image.load()

        for (x, y), color_data in hist.items():
            try:
                pixels[x, y] = self._calculate_pixel_color(color_data)
            except (ValueError, ZeroDivisionError, TypeError):
                pixels[x, y] = (0, 0, 0)

        return image

    def _calculate_pixel_color(self, color_data: dict) -> tuple:
        count = color_data["count"]
        r_sum, g_sum, b_sum = color_data["color"]
        # Средний цвет
        avg_r = self._avg_color(r_sum, count)
        avg_g = self._avg_color(g_sum, count)
        avg_b = self._avg_color(b_sum, count)

        # Яркость на основе count
        brightness = self._brightness(count)

        brightness = self._gamma_correction(brightness)  # гамма-коррекция

        r = self._rgb_color(avg_r, brightness)
        g = self._rgb_color(avg_g, brightness)
        b = self._rgb_color(avg_b, brightness)

        return (r, g, b)

    def _gamma_correction(self, brightness: float) -> float:
        return brightness ** (1.0 / self.gamma)

    @staticmethod
    def _avg_color(color_sum: float, count: int) -> float:
        return color_sum / count

    @staticmethod
    def _brightness(count: int) -> float:
        brightness_scale = 10
        # Добавляем 1, что бы логарифм не дал ошибку
        return min(1.0, math.log(count + 1) / brightness_scale)

    @staticmethod
    def _rgb_color(avg_color: float, brightness: float) -> int:
        rgb_max_size = 255
        return int(avg_color * brightness * rgb_max_size)
