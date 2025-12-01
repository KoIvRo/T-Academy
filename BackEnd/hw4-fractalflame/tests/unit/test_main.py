import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from main import main


class TestMain:
    """Тест файла main."""

    @patch("main.Config")
    def test_main_calls_config(self, mock_config: Mock) -> None:
        """Проверяет создание конфига."""
        main()
        mock_config.assert_called_once()

    @patch("main.Config")
    def test_main_loads_config(self, mock_config: Mock) -> None:
        """Проверяет загрузку конфига."""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance

        main()
        mock_config_instance.load_with_priority.assert_called_once()

    @patch("main.FractalEngine")
    def test_main_generates_fractal(self, mock_engine: Mock) -> None:
        """Проверяет генерацию фрактала."""
        mock_engine_instance = Mock()
        mock_engine.return_value = mock_engine_instance

        main()
        mock_engine_instance.generate.assert_called_once()

    @patch("main.FractalEngine")
    @patch("main.ImageExporter")
    def test_main_saves_image(self, mock_exporter: Mock, mock_engine: Mock) -> None:
        """Проверяет сохранение изображения."""
        mock_exporter_instance = Mock()
        mock_exporter.return_value = mock_exporter_instance
        mock_engine_instance = Mock()
        mock_engine.return_value = mock_engine_instance
        mock_hist = Mock()
        mock_engine_instance.generate.return_value = mock_hist

        main()
        mock_exporter_instance.save.assert_called_once_with(mock_hist.data)

    def test_main_returns_zero_on_success(self) -> None:
        """Проверяет возврат 0 при успехе."""
        with (
            patch("main.Config"),
            patch("main.FractalEngine"),
            patch("main.ImageExporter"),
        ):
            result = main()
            assert result == 0
