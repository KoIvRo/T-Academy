from dataclasses import dataclass


@dataclass
class Point:
    """Класс для точки."""

    x: int
    y: int


@dataclass
class Color:
    """Класс для цвета."""

    r: float
    g: float
    b: float
