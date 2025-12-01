import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from image import ImageExporter


class TestImageExporter:
    """Тесты для класса ImageExporter."""

    def test_exporter_initialization(self) -> None:
        """Проверяет инициализацию экспортера."""
        test_width = 800
        test_height = 600
        test_gamma = 2.2
        test_path = "test.png"

        exporter = ImageExporter(test_width, test_height, test_gamma, test_path)

        assert exporter.width == test_width
        assert exporter.height == test_height
        assert exporter.gamma == test_gamma
        assert exporter.path == test_path

    def test_avg_color_calculation(self) -> None:
        """Проверяет расчет среднего цвета."""
        test_color_sum = 10.0
        test_count = 5
        test_avg_color = 2

        result = ImageExporter._avg_color(test_color_sum, test_count)

        assert result == test_avg_color

    def test_brightness_calculation(self) -> None:
        """Проверяет расчет яркости."""
        test_count = 10

        result = ImageExporter._brightness(test_count)

        assert 0 <= result <= 1.0

    def test_rgb_color_calculation(self) -> None:
        """Проверяет преобразование в RGB."""
        test_avg_color = 0.5
        test_brightness = 0.8
        test_color_max = 255

        result = ImageExporter._rgb_color(test_avg_color, test_brightness)

        assert 0 <= result <= test_color_max

    def test_gamma_correction(self) -> None:
        """Проверяет гамма-коррекцию."""
        test_brightness = 0.5
        test_gamma = 2.2

        exporter = ImageExporter(800, 600, test_gamma, "test.png")
        result = exporter._gamma_correction(test_brightness)

        assert 0 <= result <= 1.0

    @patch("image.Image.new")
    @patch("image.logger")
    def test_save_success(self, mock_logger: Mock, mock_image_new: Mock) -> None:
        """Проверяет успешное сохранение изображения."""
        test_hist = {(1, 1): {"count": 5, "color": (10.0, 20.0, 30.0)}}
        mock_image = Mock()
        mock_image_new.return_value = mock_image

        exporter = ImageExporter(800, 600, 2.2, "test.png")
        with patch.object(exporter, "_hist_to_image", return_value=mock_image):
            exporter.save(test_hist)

        mock_image.save.assert_called_once_with("test.png")
        mock_logger.info.assert_called_once_with(
            "Изображение сохранено в файл test.png"
        )

    @patch("image.logger")
    def test_save_handles_permission_error(self, mock_logger: Mock) -> None:
        """Проверяет обработку ошибки прав доступа."""
        test_hist = {(1, 1): {"count": 5, "color": (10.0, 20.0, 30.0)}}

        exporter = ImageExporter(800, 600, 2.2, "test.png")
        with patch.object(
            exporter, "_hist_to_image", side_effect=PermissionError("No permission")
        ):
            exporter.save(test_hist)

        mock_logger.critical.assert_called_once()

    def test_hist_to_image_handles_invalid_data(self) -> None:
        """Проверяет обработку невалидных данных в гистограмме."""
        test_hist = {
            (1, 1): {"count": 5, "color": (10.0, 20.0, 30.0)},
            (2, 2): {
                "count": 0,
                "color": (0.0, 0.0, 0.0),
            },  # count = 0 вызовет ZeroDivisionError
        }

        exporter = ImageExporter(800, 600, 2.2, "test.png")
        result = exporter._hist_to_image(test_hist)

        assert isinstance(result, type(ImageExporter(1, 1, 1, "")._hist_to_image({})))

    def test_hist_to_image_with_valid_data(self) -> None:
        """Проверяет создание изображения с валидными данными."""
        test_hist = {(1, 1): {"count": 5, "color": (10.0, 20.0, 30.0)}}

        exporter = ImageExporter(800, 600, 2.2, "test.png")
        result = exporter._hist_to_image(test_hist)

        assert isinstance(result, type(ImageExporter(1, 1, 1, "")._hist_to_image({})))

    @patch("image.logger")
    def test_save_handles_is_a_directory_error(self, mock_logger: Mock) -> None:
        """Проверяет обработку ошибки когда путь это директория."""
        test_hist = {(1, 1): {"count": 5, "color": (10.0, 20.0, 30.0)}}

        exporter = ImageExporter(800, 600, 2.2, "test.png")
        with patch.object(exporter, "_hist_to_image", side_effect=IsADirectoryError()):
            exporter.save(test_hist)

        mock_logger.critical.assert_called_once()
