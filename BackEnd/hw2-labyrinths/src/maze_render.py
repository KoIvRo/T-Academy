from maze import Maze
from cell import CellType


class UnicodeRender:
    @staticmethod
    def render(maze: Maze) -> None:
        wall_map = UnicodeRender._get_unicode_map(maze)
        UnicodeRender._apply_unicode_wall(maze, wall_map)

    @staticmethod
    def _apply_unicode_wall(maze: Maze, wall_map: list[list]) -> None:
        unicode_chars = {
            (0, 0, 0, 0): " ",
            (1, 0, 0, 0): "╵",
            (0, 1, 0, 0): "╶",
            (0, 0, 1, 0): "╷",
            (0, 0, 0, 1): "╴",
            (0, 0, 1, 1): "┐",
            (0, 1, 1, 0): "┌",
            (1, 0, 0, 1): "┘",
            (1, 1, 0, 0): "└",
            (1, 1, 1, 0): "├",
            (1, 0, 1, 1): "┤",
            (1, 1, 0, 1): "┴",
            (0, 1, 1, 1): "┬",
            (1, 0, 1, 0): "│",
            (0, 1, 0, 1): "─",
            (1, 1, 1, 1): "┼",
        }
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell.type == CellType.WALL:
                    # У display есть setter, присвоить не unicode нельзя
                    # Cм. cell.py
                    cell.display = unicode_chars[wall_map[y][x]]

    @staticmethod
    def _get_unicode_map(maze: Maze) -> list[list]:
        wall_map = []
        for y in range(maze.height):
            row = []
            for x in range(maze.width):
                # Для каждой клетки набираем список из 0 1
                # Далее этот список будет преобразован в юникод символы
                symb = []
                for (
                    dx,
                    dy,
                ) in Maze.DIRECTIONS:  # Важен порядок добавления 1 или 0 в symb
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < maze.width and 0 <= ny < maze.height:
                        if (
                            maze.get_cell(x, y).type == CellType.WALL
                            and maze.get_cell(nx, ny).type == CellType.WALL
                        ):
                            symb.append(1)
                            continue
                    symb.append(0)
                row.append(tuple(symb))
            wall_map.append(row)
        return wall_map