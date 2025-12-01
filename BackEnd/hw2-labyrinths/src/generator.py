import random

from cell import CellType
from generation_algorithms import DFS, Prim
from maze import Maze


class Generator:
    # От 1 до 10
    TERRAIN_CHANCE: float = 3

    @staticmethod
    def generate(width: int, height: int, alg: str, terrain: None | int = None) -> Maze:
        # Добавить 2 для краев лабиринта
        # В том числе тобы пользователю было удобно считать клетки не начиная с 0
        # Например (1,1) даст лабиринта с 1 клеткой в центре
        maze = Maze(width + 2, height + 2)

        Generator._choose_algorithm(maze, alg)

        Generator._fix_edge(maze)
        if terrain:
            Generator._add_terrain(maze)

        return maze

    @staticmethod
    def _choose_algorithm(maze: Maze, alg: str) -> None:
        if alg == "dfs":
            DFS.dfs_generate(maze)
        elif alg == "prim":
            Prim.prim_generate(maze)
        else:
            raise ValueError("Неизвестный алгоритм. Пожалуйста используйте: dfs, prim")

    # При четных размерах стены дублируются в связи с тем, что в генерации я использую шаги по 2 клетки
    # Функция нужна что бы убрать двойные стены в случае их наличия
    @staticmethod
    def _fix_edge(maze):
        if maze.width % 2 == 0:
            for y in range(1, maze.height - 1):
                if maze.get_cell(maze.width - 3, y).display != "#":
                    maze.set_cell(maze.width - 2, y, CellType.SPACE)

        if maze.height % 2 == 0:
            for x in range(1, maze.width - 1):
                if maze.get_cell(x, maze.height - 3).display != "#":
                    maze.set_cell(x, maze.height - 2, CellType.SPACE)

    @staticmethod
    def _add_terrain(maze):
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.get_cell(x, y).type == CellType.SPACE:
                    if random.randint(1, 10) < Generator.TERRAIN_CHANCE:
                        maze.set_cell(
                            x,
                            y,
                            random.choice(
                                [CellType.SAND, CellType.SWAMP, CellType.COIN]
                            ),
                        )