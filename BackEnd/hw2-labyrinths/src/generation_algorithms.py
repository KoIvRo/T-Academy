import random
from maze import Maze
from cell import CellType


class Prim:
    @staticmethod
    def prim_generate(maze: Maze) -> None:
        frontier = []
        visited = set()
        start_x, start_y = 1, 1

        Prim._prim_visited(maze, start_x, start_y, visited, frontier)

        while frontier:
            rand_ind = random.randint(0, len(frontier)-1)
            frontier[rand_ind], frontier[-1] = frontier[-1], frontier[rand_ind]
            wall_x, wall_y, cell_x, cell_y = frontier[-1]
            frontier.pop()

            if (cell_x, cell_y) not in visited:
                maze.set_cell(wall_x, wall_y, CellType.SPACE)
                Prim._prim_visited(maze, cell_x, cell_y, visited, frontier)
    
    @staticmethod
    def _prim_visited(maze: Maze, x: int, y: int, visited: set, frontier: list) -> None:
        maze.set_cell(x, y, CellType.SPACE)
        visited.add((x, y))

        for dx, dy in [(2, 0), (0, 2), (-2, 0), (0, -2)]:
            nx, ny = x + dx, y + dy
            if maze.in_maze(nx, ny):
                frontier.append((x + dx//2, y + dy//2, nx, ny))


class DFS:
    @staticmethod
    def dfs_generate(maze) -> None:
        visited = set()
        start_x, start_y = 1, 1

        DFS._dfs_visited(maze, start_x, start_y, visited)


    @staticmethod
    def _dfs_visited(maze, x: int, y: int, visited: set) -> None:
        visited.add((x, y))
        maze.set_cell(x, y, CellType.SPACE)

        directions = DFS._dfs_get_random_directions()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if maze.in_maze(nx, ny) and ((nx, ny) not in visited):
                maze.set_cell(x + dx//2, y + dy//2, CellType.SPACE)
                visited.add((x + dx//2, y + dy//2))
                DFS._dfs_visited(maze, nx, ny, visited)
            

    @staticmethod
    def _dfs_get_random_directions():
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        random.shuffle(directions)

        return directions
