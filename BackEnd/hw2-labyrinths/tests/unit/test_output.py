import os
import sys
import unittest
from unittest.mock import MagicMock, patch, call
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from file_manager import Input, Output
from maze import Maze, CellType

class TestOutput(unittest.TestCase):
    @patch("builtins.print")
    def test_print_cl(self, mock_print):
        maze = Maze(2, 2)
        for y in range(2):
            for x in range(2):
                maze.set_cell(x, y, CellType.WALL)
        
        Output.cl_print(maze)

        expected_calls = [
            call("#", end=""), call("#", end=""), call(),
            call("#", end=""), call("#", end=""), call()
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_read_simple_maze(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("##\n##")
            temp_path = f.name
        
        maze = Input.input_from_file(temp_path)
        self.assertEqual(maze.width, 2)
        self.assertEqual(maze.height, 2)
        os.unlink(temp_path)