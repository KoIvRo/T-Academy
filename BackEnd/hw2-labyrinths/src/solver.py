from maze import Maze
from cell import CellType
from solve_algorithms import Dijkstra, Astar


class Solver:
    def __init__(self, maze, start: str, end: str, alg: str):
        self.maze: Maze = maze
        self.start, self.end = PointSetter.set_points(maze, start, end)
        self.algorithm = alg

    def execute(self) -> bool:
        Algrorithm = self._choose_algorithm(self.algorithm)
        path = Algrorithm(self.maze, self.start, self.end).solve()
        if path:
            self.maze.mark_path_to_maze(path)
            return True
        return False

    @staticmethod
    def _choose_algorithm(str_alg) -> type:
        algorithms = {
            "dijkstra": Dijkstra,
            "astar": Astar
        }
        if str_alg in algorithms:
            return algorithms[str_alg]
        raise ValueError("Неизвестный алгоритм. Пожалуйста используйте: dijkstra, astar")

class PointSetter:
    @staticmethod
    def set_points(maze: Maze, start: str, end: str) -> tuple[tuple, tuple]:
        start = PointSetter._validate_points(maze, start)
        end = PointSetter._validate_points(maze, end)

        maze.set_cell(start[0], start[1], CellType.START)
        maze.set_cell(end[0], end[1], CellType.END)

        return start, end

    @staticmethod
    def _validate_points(maze: Maze, coord: str) -> tuple:
        coord = list(map(int, coord.split(",")))

        if len(coord) < 2 or len(coord) > 2:
            raise ValueError("Неверный формат входных данных. Ожидается: x,y")

        if maze.is_cell_possible(coord[0], coord[1]):
            return tuple(coord)
        else:
            raise ValueError("Ошибка в координатах")
