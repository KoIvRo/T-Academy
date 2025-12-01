import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from maze import CellType, Maze
from maze_render import UnicodeRender


class TestMaze(unittest.TestCase):
    def test_maze_creation(self):
        maze = Maze(5, 5)
        self.assertEqual(maze.width, 5)
        self.assertEqual(maze.height, 5)

    def test_cell_operations(self):
        maze = Maze(3, 3)

        maze.set_cell(1, 1, CellType.PATH)
        self.assertEqual(maze.get_cell(1, 1).type, CellType.PATH)

        maze.set_cell(0, 0, CellType.WALL)
        self.assertEqual(maze.get_cell(0, 0).type, CellType.WALL)

    def test_is_cell_possible(self):
        maze = Maze(3, 3)
        maze.set_cell(1, 1, CellType.PATH)

        self.assertTrue(maze.is_cell_possible(1, 1))
        self.assertFalse(maze.is_cell_possible(0, 0))

class TestUnicodeRender(unittest.TestCase):
    @patch("maze_render.UnicodeRender._get_unicode_map")
    @patch("maze_render.UnicodeRender._apply_unicode_wall")
    def test_unicode(self, apply, get):
        maze = Maze(3, 3)
        UnicodeRender.render(maze)
        apply.assert_called_once_with(maze, get.return_value)
        get.assert_called_once_with(maze)

    def test_get_unicode_map(self):
        maze = Maze(3, 3)
        result = UnicodeRender._get_unicode_map(maze)
        self.assertEqual(result[0][0], (0, 1, 1, 0))

    def test_apply_unicode(self):
        maze = Maze(3, 3)
        wall_map = UnicodeRender._get_unicode_map(maze)
        UnicodeRender._apply_unicode_wall(maze, wall_map)
        self.assertEqual(maze.get_cell(0, 0).display, "┌")