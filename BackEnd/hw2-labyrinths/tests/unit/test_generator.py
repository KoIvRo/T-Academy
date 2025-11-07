import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from generator import Generator
from generation_algorithms import DFS, Prim
from maze import Maze, CellType

class TestGenerator(unittest.TestCase):

    @patch("generation_algorithms.DFS.dfs_generate")
    def test_dfs(self, dfs):
        maze = Generator.generate(2, 2, "dfs")
        dfs.assert_called_once()
        self.assertEqual(maze.width, 4)
        self.assertEqual(maze.height, 4)

    @patch("generation_algorithms.Prim.prim_generate")
    def test_prim(self, prim):
        maze = Generator.generate(2, 2, "prim")
        prim.assert_called_once()
        self.assertEqual(maze.width, 4)
        self.assertEqual(maze.height, 4)

    def test_generate_unknown_algorithm(self):
        with self.assertRaises(ValueError):
            Generator.generate(2, 2, "unknown")

    def test_fix_edge(self):
        maze = Maze(6, 4)
        maze.set_cell(3, 1, CellType.SPACE)
        Generator._fix_edge(maze)
        self.assertEqual(maze.get_cell(3, 2).type, CellType.SPACE)

    @patch("random.randint")
    @patch("random.choice")
    def test_terrain(self, mock_choice, mock_randint):
        mock_choice.return_value = CellType.SAND
        mock_randint.return_value = 1
        maze = Maze(3,3)
        maze.set_cell(1,1,CellType.SPACE)
        Generator._add_terrain(maze)
        self.assertEqual(maze.get_cell(1,1).type, CellType.SAND)