import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.UI import GameUI

class TestUI(unittest.TestCase):

    @patch('os.system')
    @patch('builtins.print')
    def test_get_game_stat_full_info(self, mock_print, mock_system):
        ui = GameUI()
        
        mock_game_get_stat = {
            "word": "собака",
            "category": "животные",
            "cur_word": "c*б*к*",
            "tuple_attempts_and_sub_attemps": (5, (6, 5, 3, 2, 1, 0)),
            "letters": None,
            "hint": "Друг человека",
            "state": False
        }
        
        ui.print_game_stat(mock_game_get_stat)

        mock_system.assert_called_once_with("cls")

        mock_print.assert_called()
        calls = mock_print.call_args_list

        self.assertTrue(any("___________" in str(call) for call in calls))
        
        self.assertTrue(any("Категория: животные" in str(call) for call in calls))
        
        self.assertTrue(any("Слово: c*б*к*" in str(call) for call in calls))
        self.assertTrue(any("Попыток осталось: 5" in str(call) for call in calls))

        self.assertTrue(any("Использованные буквы:" in str(call) for call in calls))
        
        self.assertTrue(any("Друг человека" in str(call) for call in calls))


    @patch('os.system')
    @patch('builtins.print')
    def test_get_game_stat_no_hint(self, mock_print, mock_system):
        ui = GameUI()
        
        mock_game_get_stat = {
            "word": "собака",
            "category": "животные",
            "cur_word": "c*ба*а",
            "tuple_attempts_and_sub_attemps": (5, (6, 5, 3, 2, 1, 0)),
            "letters": None,
            "hint": None,
            "state": False
        }
        
        ui.print_game_stat(mock_game_get_stat)

        mock_print.assert_called()
        calls = mock_print.call_args_list

        self.assertTrue(any("Подсказка:" not in str(call) for call in calls))


    @patch('os.system')
    @patch('builtins.print')
    def test_final_stat_lose(self, mock_print, mock_system):
        ui = GameUI()
        mock_game_stat = {
            "word": "собака",
            "category": "животные",
            "cur_word": "c*ба*а",
            "tuple_attempts_and_sub_attemps": (5, (6, 5, 3, 2, 1, 0)),
            "letters": None,
            "hint": None,
            "state": False
        }
        ui.print_final_stat(mock_game_stat)
        mock_print.assert_called()
        calls = mock_print.call_args_list

        self.assertTrue(any("Вы победили:" not in str(call) for call in calls))

    @patch('os.system')
    @patch('builtins.print')
    def test_final_stat_win(self, mock_print, mock_system):
        ui = GameUI()
        mock_game_stat = {
            "word": "собака",
            "category": "животные",
            "cur_word": "c*ба*а",
            "tuple_attempts_and_sub_attemps": (5, (6, 5, 3, 2, 1, 0)),
            "letters": None,
            "hint": None,
            "state": True
        }

        ui.print_final_stat(mock_game_stat)
        mock_print.assert_called()
        calls = mock_print.call_args_list

        self.assertTrue(any("Вы победили" in str(call) for call in calls))

    
    def test_stage(self):
        ui = GameUI()
        ui._update_stage_by_attemps((7, (6, 5, 4)))

        self.assertTrue(ui._last_attempts, None)


    def test_stage_up(self):
        ui = GameUI()
        ui._update_stage_by_attemps((7, (6, 5, 4)))
        ui._update_stage_by_attemps((6, (6, 5, 4)))

        self.assertTrue(ui._current_stage, 1)
        self.assertTrue(ui._last_attempts, 7)