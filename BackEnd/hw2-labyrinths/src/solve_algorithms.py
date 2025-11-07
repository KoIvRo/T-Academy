import queue
from maze import Maze
from abc import ABC, abstractmethod
from path import Path

class Algorithm(ABC):
    def __init__(self, maze: Maze, start: tuple, end: tuple):
        self.maze = maze
        self.start = start
        self.end = end

    @abstractmethod
    def solve(solver) -> Path | None:
        pass


class Dijkstra(Algorithm):
    def __init__(self, maze: Maze, start: tuple, end: tuple):
        super().__init__(maze, start, end)

        self.distance: dict[tuple[int, int]: int] = InitializationServises.initialize_distance(self.maze, self.start)
        self.previous: dict[tuple[int, int]: tuple[int, int]] = InitializationServises.initialize_previous(self.maze)
        self.visited = set()
        self.pr_queue = queue.PriorityQueue()

    def solve(self) -> Path | None:
        self.pr_queue.put((0, self.start))

        while not self.pr_queue.empty():
            cur_cell_dist, cur_cell_coord = self.pr_queue.get()

            if cur_cell_coord in self.visited:
                continue

            if cur_cell_coord == self.end:
                ready_path = Path.collect_path(self.start, self.end, self.previous)
                return Path(ready_path, self.start, self.end)

            self.visited.add(cur_cell_coord)

            for neighbour in self.maze.get_neighbours(cur_cell_coord):
                self._process_neighbour(neighbour, cur_cell_dist, cur_cell_coord)

        return None

    def _process_neighbour(self, neighbour, cur_cell_dist, cur_cell_coord) -> None:
        if not self.maze.is_cell_possible(neighbour[0], neighbour[1]):
            return
        if neighbour in self.visited:
            return
                
        neighbour_cost = self.maze.get_cell(neighbour[0], neighbour[1]).cost
        new_dist = cur_cell_dist + neighbour_cost
        if new_dist < self.distance[neighbour]:
            self.distance[neighbour] = new_dist
            self.previous[neighbour] = cur_cell_coord
            self.pr_queue.put((new_dist, neighbour))


class Astar(Algorithm):
    def __init__(self, maze: Maze, start: tuple, end: tuple):
        super().__init__(maze, start, end)

        self.real_distance = InitializationServises.initialize_distance(self.maze, self.start)
        self.heuristic_distance: dict[tuple[int, int]: int] = InitializationServises.initialize_distance(self.maze, self.start)
        self.previous: dict[tuple[int, int]: tuple[int, int]] = InitializationServises.initialize_previous(self.maze)
        self.visited = set()
        self.pr_queue = queue.PriorityQueue()

    def solve(self) -> Path | None:
        self.heuristic_distance[self.start] = Astar._heruistic(self.start, self.end)
        self.pr_queue.put((self.heuristic_distance[self.start], self.start))

        while not self.pr_queue.empty():
            _, cur_cell_coord = self.pr_queue.get()

            if cur_cell_coord in self.visited:
                continue

            if cur_cell_coord == self.end:
                ready_path = Path.collect_path(self.start, self.end, self.previous)
                return Path(ready_path, self.start, self.end)

            self.visited.add(cur_cell_coord)

            for neighbour in self.maze.get_neighbours(cur_cell_coord):
                self._poccess_neighbour(neighbour, cur_cell_coord)

        return None

    def _poccess_neighbour(self, neighbour, cur_cell_coord) -> None:
        if not self.maze.is_cell_possible(neighbour[0], neighbour[1]):
            return
        if neighbour in self.visited:
            return
        neighbour_cost = self.maze.get_cell(neighbour[0], neighbour[1]).cost

        new_real_distance = self.real_distance[cur_cell_coord] + neighbour_cost

        if new_real_distance < self.real_distance[neighbour]:
            self.previous[neighbour] = cur_cell_coord
            self.real_distance[neighbour] = new_real_distance
            self.heuristic_distance[neighbour] = new_real_distance + Astar._heruistic(neighbour, self.end)
            self.pr_queue.put((self.heuristic_distance[neighbour], neighbour))

    @staticmethod
    def _heruistic(cell, end):
        return abs(cell[0] - end[0]) + abs(cell[1] - end[1])


class InitializationServises:
    @staticmethod
    def initialize_previous(maze: Maze):
        previous = {}
        for y in range(maze.height):
            for x in range(maze.width):
                previous[(x, y)] = None
        return previous

    @staticmethod
    def initialize_distance(maze: Maze, start):
        distance = {}
        for y in range(maze.height):
            for x in range(maze.width):
                distance[(x, y)] = float('inf')
        distance[start] = 0
        return distance