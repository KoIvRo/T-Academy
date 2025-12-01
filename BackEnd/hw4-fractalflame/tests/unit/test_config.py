import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from config import Config


class TestConfig:
    """Тесты для класса Config."""

    def test_config_default_values(self) -> None:
        """Проверяет значения по умолчанию."""
        default_width = 1920
        default_height = 1080
        default_seed = 5.1234
        default_iterations = 250000
        default_gamma = 2.2
        config = Config()
        assert config.width == default_width
        assert config.height == default_height
        assert config.seed == default_seed
        assert config.iteration_count == default_iterations
        assert config.output_path == "result.png"
        assert config.threads == 1
        assert config.gamma == default_gamma
        assert config.symmetry_level == 1

    def test_parse_functions_valid_string(self) -> None:
        """Проверяет парсинг строки функций."""
        functions_str = "swirl:1.0,horseshoe:0.8"
        result = Config._parse_functions(functions_str)
        expected = [
            {"name": "swirl", "weight": 1.0},
            {"name": "horseshoe", "weight": 0.8},
        ]
        assert result == expected

    def test_parse_affine_params_valid_string(self) -> None:
        """Проверяет парсинг аффинных параметров."""
        params_str = "1.0,2.0,3.0,4.0,5.0,6.0"
        result = Config._parse_affine_params(params_str)
        expected = {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0, "e": 5.0, "f": 6.0}
        assert result == expected

    @patch("config.Config._parse_cli_args")
    def test_load_with_priority_no_config_file(self, mock_parse_args: Mock) -> None:
        """Проверяет загрузку без конфиг файла."""
        # Создаем правильный объект args
        mock_args = Mock(
            spec=[
                "config",
                "width",
                "height",
                "seed",
                "iteration_count",
                "output_path",
                "threads",
                "gamma",
                "symmetry_level",
                "functions",
                "affine_params",
            ]
        )
        mock_args.config = None
        mock_args.width = None
        mock_args.height = None
        mock_args.seed = None
        mock_args.iteration_count = None
        mock_args.output_path = None
        mock_args.threads = None
        mock_args.gamma = None
        mock_args.symmetry_level = None
        mock_args.functions = None
        mock_args.affine_params = None
        mock_parse_args.return_value = mock_args

        config = Config()
        config.load_with_priority()

        mock_parse_args.assert_called_once()

    @patch("config.Config._apply_json")
    @patch("config.Config._parse_cli_args")
    def test_load_with_priority_with_config_file(
        self, mock_parse_args: Mock, mock_apply_json: Mock
    ) -> None:
        """Проверяет загрузку с конфиг файлом."""
        mock_args = Mock(
            spec=[
                "config",
                "width",
                "height",
                "seed",
                "iteration_count",
                "output_path",
                "threads",
                "gamma",
                "symmetry_level",
                "functions",
                "affine_params",
            ]
        )
        mock_args.config = "config.json"
        mock_args.width = None
        mock_args.height = None
        mock_args.seed = None
        mock_args.iteration_count = None
        mock_args.output_path = None
        mock_args.threads = None
        mock_args.gamma = None
        mock_args.symmetry_level = None
        mock_args.functions = None
        mock_args.affine_params = None
        mock_parse_args.return_value = mock_args

        config = Config()
        with patch("config.Config._read_json") as mock_read_json:
            mock_read_json.return_value = {"width": 1000}
            config.load_with_priority()

        mock_read_json.assert_called_once_with("config.json")
        mock_apply_json.assert_called_once()

    def test_apply_cli_args_updates_values(self) -> None:
        """Проверяет применение CLI аргументов."""
        test_width = 800
        test_height = 600
        test_seed = 1.0
        test_iterations = 1000
        test_threads = 4
        test_gamma = 1.8
        test_symmetry = 2
        config = Config()
        mock_args = Mock()
        mock_args.width = test_width
        mock_args.height = test_height
        mock_args.seed = test_seed
        mock_args.iteration_count = test_iterations
        mock_args.output_path = "test.png"
        mock_args.threads = test_threads
        mock_args.gamma = test_gamma
        mock_args.symmetry_level = test_symmetry
        mock_args.functions = None
        mock_args.affine_params = None

        config._apply_cli_args(mock_args)

        assert config.width == test_width
        assert config.height == test_height
        assert config.seed == test_seed
        assert config.iteration_count == test_iterations
        assert config.output_path == "test.png"
        assert config.threads == test_threads
        assert config.gamma == test_gamma
        assert config.symmetry_level == test_symmetry

    def test_apply_json_updates_values(self) -> None:
        """Проверяет применение JSON конфигурации."""
        test_width = 800
        test_height = 600
        test_seed = 2.0
        test_iterations = 5000
        test_threads = 2
        test_gamma = 2.0
        test_symmetry = 3
        config = Config()
        json_config = {
            "width": test_width,
            "height": test_height,
            "seed": test_seed,
            "iteration_count": test_iterations,
            "output_path": "json_test.png",
            "threads": test_threads,
            "gamma": test_gamma,
            "symmetry_level": test_symmetry,
            "functions": [{"name": "linear", "weight": 1.0}],
            "affine_params": {
                "a": 1.0,
                "b": 1.0,
                "c": 1.0,
                "d": 1.0,
                "e": 1.0,
                "f": 1.0,
            },
        }

        config._apply_json(json_config)

        assert config.width == test_width
        assert config.height == test_height
        assert config.seed == test_seed
        assert config.iteration_count == test_iterations
        assert config.output_path == "json_test.png"
        assert config.threads == test_threads
        assert config.gamma == test_gamma
        assert config.symmetry_level == test_symmetry
        assert config.functions == [{"name": "linear", "weight": 1.0}]
        assert config.affine_params == {
            "a": 1.0,
            "b": 1.0,
            "c": 1.0,
            "d": 1.0,
            "e": 1.0,
            "f": 1.0,
        }
