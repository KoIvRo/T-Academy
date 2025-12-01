import os
import sys
import tempfile
import unittest
from unittest.mock import call, patch

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from file_manager import Input, Output
from maze import CellType, Maze


class TestOutput(unittest.TestCase):
    @patch("builtins.print")
    def test_print_cl(self, mock_print):
        maze = Maze(4, 4)
        for y in range(4):
            for x in range(4):
                maze.set_cell(x, y, CellType.WALL)

        Output.cl_print(maze)

        expected_calls = []
        for y in range(4):
            for x in range(4):
                expected_calls.append(call("#", end=""))
            expected_calls.append(call())
        
        mock_print.assert_has_calls(expected_calls)

    def test_read_simple_maze(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("###\n###\n###")
            temp_path = f.name

        try:
            maze = Input.input_from_file(temp_path)
            self.assertEqual(maze.width, 3)
            self.assertEqual(maze.height, 3)
        finally:
            os.unlink(temp_path)