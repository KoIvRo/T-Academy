import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from solver import Solver, PointSetter
from maze import Maze, CellType
from solve_algorithms import Astar, Dijkstra
from path import Path

class TestPointSetter(unittest.TestCase):
    def test_point_validation(self):
        maze = Maze(4, 4)
        for y in range(maze.height):
            for x in range(maze.width):
                maze.set_cell(x, y, CellType.PATH)

        start, end = PointSetter.set_points(maze, "1,1", "2,2")

        self.assertEqual(start, (1,1))
        self.assertEqual(end, (2,2))

    def test_point_error(self):
        maze = Maze(2,2)
        with self.assertRaises(ValueError):
            PointSetter.set_points(maze, "1,1", "2,2")

    @patch('solve_algorithms.Astar.solve')
    def test_solver_astar(self, astar_mock):
        fake_path = Path(
            path=[(1,1), (1,2), (2,2)], 
            start=(1,1), 
            end=(2,2)
        )
        astar_mock.return_value = fake_path
        maze = Maze(4,4)
        for y in range(maze.height):
            for x in range(maze.width):
                maze.set_cell(x, y, CellType.PATH)
        
        maze_solver = Solver(maze, "1,1", "2,2", "astar")
        result = maze_solver.execute()
        
        assert result == True

    @patch('solve_algorithms.Dijkstra.solve')
    def test_solver_djkstra(self, dijkstra_mock):
        fake_path = Path(
            path=[(1,1), (1,2), (2,2)], 
            start=(1,1), 
            end=(2,2)
        )
        dijkstra_mock.return_value = fake_path
        maze = Maze(4,4)
        for y in range(maze.height):
            for x in range(maze.width):
                maze.set_cell(x, y, CellType.PATH)
        
        maze_solver = Solver(maze, "1,1", "2,2", "dijkstra")
        result = maze_solver.execute()
        
        assert result == True

    def test_solver_unknown_algorithm(self):
        maze = Maze(4,4)
        for y in range(maze.height):
            for x in range(maze.width):
                maze.set_cell(x, y, CellType.PATH)

        with self.assertRaises(ValueError):
            solver = Solver(maze, "1,1", "2,2", "None").execute()