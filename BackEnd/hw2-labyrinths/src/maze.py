from cell import Cell, CellType
from path import Path


class Maze:
    # Очень важен порядок
    # Менять нельзя!!!
    DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, width, height):
        Maze._validate_size(width, height)
        self.width = width
        self.height = height
        self._map = [
            [Cell(CellType.WALL) for _ in range(self.width)] for _ in range(self.height)
        ]

    @staticmethod
    def _validate_size(width, height):
        if width <= 2 or height <= 2:
            raise ValueError(
                f"Заданы неверные размеры ширина: {width}, высота: {height}"
            )


    # Для проходимой части лабиринта
    def in_maze(self, x, y):
        return 0 < x < self.width - 1 and 0 < y < self.height - 1

    def set_cell(self, x, y, type: CellType):
        if self.in_maze(x, y):
            self._map[y][x] = Cell(type)

    def get_cell(self, x, y):
        return self._map[y][x]

    def is_cell_possible(self, x, y) -> bool:
        if self.in_maze(x, y) and self._map[y][x].cost != float("inf"):
            return True
        return False

    def get_neighbours(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = cell
        neighbors = []

        for dx, dy in Maze.DIRECTIONS:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < self.width
                and 0 <= ny < self.height
                and self.is_cell_possible(nx, ny)
            ):
                neighbors.append((nx, ny))

        return neighbors

    def mark_path_to_maze(self, path: Path) -> None:
        for x, y in path.ready_path:
            self.set_cell(x, y, CellType.PATH)
        self.set_cell(path.start[0], path.start[1], CellType.START)
        self.set_cell(path.end[0], path.end[1], CellType.END)
