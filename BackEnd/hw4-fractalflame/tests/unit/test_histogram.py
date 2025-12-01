import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from histogram import Histogram
from models import Color, Point


class TestHistogram:
    """Тесты для класса Histogram."""

    def test_histogram_initialization(self) -> None:
        """Проверяет инициализацию гистограммы."""
        test_width = 800
        test_height = 600
        test_gamma = 2.0
        test_symmetry_level = 2
        hist = Histogram(
            width=test_width,
            height=test_height,
            gamma=test_gamma,
            symmetry_level=test_symmetry_level,
        )
        assert hist.width == test_width
        assert hist.height == test_height
        assert hist.gamma == test_gamma
        assert hist.symmetry_level == test_symmetry_level
        assert hist.data == {}

    def test_add_single_point_within_bounds(self) -> None:
        """Проверяет добавление точки в пределах изображения."""
        test_width = 800
        test_height = 600
        hist = Histogram(width=test_width, height=test_height)
        point = Point(0.0, 0.0)
        color = Color(0.5, 0.5, 0.5)

        hist._add_single_point(point, color)

        assert (400, 300) in hist.data
        assert hist.data[(400, 300)]["count"] == 1
        assert hist.data[(400, 300)]["color"] == (0.5, 0.5, 0.5)

    def test_add_single_point_out_of_bounds(self) -> None:
        """Проверяет что точки вне изображения не добавляются."""
        test_width = 800
        test_height = 600
        hist = Histogram(width=test_width, height=test_height)
        point = Point(10.0, 10.0)
        color = Color(0.5, 0.5, 0.5)

        hist._add_single_point(point, color)

        assert hist.data == {}

    def test_add_single_point_increments_count(self) -> None:
        """Проверяет увеличение счетчика при добавлении в ту же точку."""
        test_width = 800
        test_height = 600
        test_count = 2
        hist = Histogram(width=test_width, height=test_height)
        point = Point(0.0, 0.0)
        color = Color(0.5, 0.5, 0.5)

        hist._add_single_point(point, color)
        hist._add_single_point(point, color)

        assert hist.data[(400, 300)]["count"] == test_count
        assert hist.data[(400, 300)]["color"] == (1.0, 1.0, 1.0)

    def test_rotate_point(self) -> None:
        """Проверяет поворот точки."""
        test_tolerance = 0.001
        hist = Histogram()
        point = Point(1.0, 0.0)

        rotated = hist._rotate_point(point, math.pi / 2)

        assert abs(rotated.x - 0.0) < test_tolerance
        assert abs(rotated.y - 1.0) < test_tolerance

    def test_add_point_handles_exception(self) -> None:
        """Проверяет обработку исключений в add_point."""
        hist = Histogram()
        with pytest.raises(AttributeError):
            hist.add_point("invalid_point", "invalid_color")
