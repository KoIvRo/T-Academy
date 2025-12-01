import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from engine import FractalEngine
from histogram import Histogram


class TestFractalEngine:
    """Тесты для класса FractalEngine."""

    def test_engine_initialization(self) -> None:
        """Проверяет инициализацию движка."""
        mock_config = Mock()
        mock_config.functions = [{"name": "linear", "weight": 1.0}]
        mock_config.affine_params = {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }

        engine = FractalEngine(mock_config)

        assert engine.config == mock_config

    def test_generate_single_thread(self) -> None:
        """Проверяет однопоточную генерацию."""
        mock_config = Mock()
        mock_config.threads = 1
        mock_config.width = 800
        mock_config.height = 600
        mock_config.gamma = 2.2
        mock_config.symmetry_level = 1
        mock_config.seed = 1.0
        mock_config.iteration_count = 100
        mock_config.functions = [{"name": "linear", "weight": 1.0}]
        mock_config.affine_params = {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }

        engine = FractalEngine(mock_config)
        result = engine.generate()

        assert isinstance(result, Histogram)

    def test_create_worker_args(self) -> None:
        """Проверяет создание аргументов для воркеров."""
        mock_config = Mock()
        mock_config.threads = 3
        mock_config.iteration_count = 100
        mock_config.functions = [{"name": "linear", "weight": 1.0}]
        mock_config.affine_params = {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }

        engine = FractalEngine(mock_config)
        args = engine._create_worker_args()

        assert all(isinstance(arg, tuple) for arg in args)

    def test_worker_function(self) -> None:
        """Проверяет функцию воркера."""
        mock_config = Mock()
        mock_config.width = 800
        mock_config.height = 600
        mock_config.gamma = 2.2
        mock_config.symmetry_level = 1
        mock_config.seed = 1.0
        mock_config.functions = [{"name": "linear", "weight": 1.0}]
        mock_config.affine_params = {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }

        engine = FractalEngine(mock_config)
        test_args = (1, 10)

        result = engine._worker(test_args)

        assert isinstance(result, Histogram)

    def test_merge_histograms(self) -> None:
        """Проверяет объединение гистограмм."""
        mock_config = Mock()
        mock_config.functions = [{"name": "linear", "weight": 1.0}]
        mock_config.affine_params = {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }

        engine = FractalEngine(mock_config)

        hist1 = Histogram()
        hist1.data = {(1, 1): {"count": 2, "color": (1.0, 1.0, 1.0)}}

        hist2 = Histogram()
        hist2.data = {(1, 1): {"count": 3, "color": (2.0, 2.0, 2.0)}}

        result = engine._merge_histograms([hist1, hist2])

        assert result.data[(1, 1)]["color"] == (3.0, 3.0, 3.0)

    def test_generate_handles_exception(self) -> None:
        """Проверяет обработку исключений в generate."""
        mock_config = Mock()
        mock_config.threads = 1
        mock_config.functions = [{"name": "linear", "weight": 1.0}]
        mock_config.affine_params = {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }

        engine = FractalEngine(mock_config)

        with patch.object(
            engine, "_single_thread_generate", side_effect=ValueError("Test error")
        ):
            result = engine.generate()
        assert result is None
