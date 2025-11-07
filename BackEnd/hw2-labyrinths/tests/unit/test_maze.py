import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from maze import Maze, CellType


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


    @patch("maze.Maze._get_unicode_map")
    @patch("maze.Maze._apply_unicode_wall")
    def test_unicode(self, apply, get):
        Maze(3,3).to_unicode_converse()
        apply.assert_called_once()
        get.assert_called_once()

    def test_get_unicode_map(self):
        self.assertEqual(Maze(3,3)._get_unicode_map()[0][0], (0,1,1,0))
    
    def test_apply_incode(self):
        maze = Maze(3,3)
        wall_map = maze._get_unicode_map()
        maze._apply_unicode_wall(wall_map)
        self.assertEqual(maze.get_cell(0,0).display, "┌")