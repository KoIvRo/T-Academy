import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from models import Color, Point
from transform import AffineTransformer, Transformations, TransformationSystem


class TestTransformations:
    """Тесты для класса Transformations."""

    def test_linear_transformation(self) -> None:
        """Проверяет линейную трансформацию."""
        test_point = Point(1.0, 2.0)
        test_color = Color(0.1, 0.2, 0.3)

        result_point, result_color = Transformations.linear(test_point, test_color)

        assert result_point.x == test_point.x
        assert result_point.y == test_point.y
        assert result_color.r == (test_color.r + 0.95) / 2
        assert result_color.g == (test_color.g + 0.85) / 2
        assert result_color.b == (test_color.b + 0.1) / 2

    def test_swirl_transformation(self) -> None:
        """Проверяет swirl трансформацию."""
        test_point = Point(1.0, 0.0)
        test_color = Color(0.1, 0.2, 0.3)

        result_point, result_color = Transformations.swirl(test_point, test_color)

        assert isinstance(result_point, Point)
        assert isinstance(result_color, Color)

    def test_horseshoe_transformation_zero_radius(self) -> None:
        """Проверяет horseshoe трансформацию с нулевым радиусом."""
        test_point = Point(0.0, 0.0)
        test_color = Color(0.1, 0.2, 0.3)

        result_point, result_color = Transformations.swirl(test_point, test_color)

        assert isinstance(result_point, Point)
        assert isinstance(result_color, Color)

    def test_sinusoidal_transformation(self) -> None:
        """Проверяет sinusoidal трансформацию."""
        test_point = Point(1.0, 2.0)
        test_color = Color(0.1, 0.2, 0.3)

        result_point, result_color = Transformations.sinusoidal(test_point, test_color)

        assert isinstance(result_point, Point)
        assert isinstance(result_color, Color)

    def test_spherical_transformation_zero_radius(self) -> None:
        """Проверяет spherical трансформацию с нулевым радиусом."""
        test_point = Point(0.0, 0.0)
        test_color = Color(0.1, 0.2, 0.3)

        result_point, result_color = Transformations.spherical(test_point, test_color)

        assert result_point.x == 0.0
        assert result_point.y == 0.0
        assert isinstance(result_color, Color)

    def test_get_variation_existing(self) -> None:
        """Проверяет получение существующей трансформации."""
        result = Transformations.get_variation("linear")
        assert result == Transformations.linear

    def test_get_variation_non_existing(self) -> None:
        """Проверяет получение несуществующей трансформации."""
        result = Transformations.get_variation("non_existing")
        assert result == Transformations.linear


class TestAffineTransformer:
    """Тесты для класса AffineTransformer."""

    def test_affine_transform(self) -> None:
        """Проверяет аффинное преобразование."""
        test_a = 0.6
        test_b = 0.6
        test_c = 0.6
        test_d = 0.6
        test_e = 0.6
        test_f = 0.6
        transformer = AffineTransformer(test_a, test_b, test_c, test_d, test_e, test_f)
        test_point = Point(2.0, 3.0)

        result = transformer.transform(test_point)

        expected_x = test_a * test_point.x + test_b * test_point.y + test_c
        expected_y = test_d * test_point.x + test_e * test_point.y + test_f
        assert result.x == expected_x
        assert result.y == expected_y


class TestTransformationSystem:
    """Тесты для класса TransformationSystem."""

    def test_transformation_system_initialization(self) -> None:
        """Проверяет инициализацию системы трансформаций."""
        test_functions = [{"name": "linear", "weight": 1.0}]
        test_affine = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0, "e": 1.0, "f": 1.0}

        system = TransformationSystem(test_functions, test_affine)

        assert system.function_params == test_functions
        assert system.function_total_weight == 1.0

    def test_choose_random_transform(self) -> None:
        """Проверяет выбор случайной трансформации."""
        test_functions = [{"name": "linear", "weight": 1.0}]
        test_affine = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0, "e": 1.0, "f": 1.0}
        system = TransformationSystem(test_functions, test_affine)

        result = system._choose_random_transform()

        assert result == "linear"
