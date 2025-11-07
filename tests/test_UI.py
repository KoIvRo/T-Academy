import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from UI import GameUI

class TestUI(unittest.TestCase):
    def test_get_len_hangman_stage(self):
        ui = GameUI()
        length = ui.get_len_hangman_stage()
        
        self.assertEqual(length, 7)

    @patch('os.system')
    @patch('builtins.print')
    def test_get_game_stat_full_info(self, mock_print, mock_system):
        ui = GameUI()
        
        mock_game = MagicMock()
        mock_game.get_picture_stage.return_value = 2
        mock_game.get_category.return_value = "животные"
        mock_game.get_cur_state_word.return_value = "с*б*ка"
        mock_game.get_attemps.return_value = 5
        mock_game.get_prev_letters.return_value = ["с", "б", "а"]
        mock_game.get_is_hint_active.return_value = True
        mock_game.get_hint.return_value = "друг человека"
        
        ui.get_game_stat(mock_game)

        mock_system.assert_called_once_with("cls")

        mock_print.assert_called()
        calls = mock_print.call_args_list

        self.assertTrue(any("___________" in str(call) for call in calls))
        
        self.assertTrue(any("Категория: животные" in str(call) for call in calls))
        
        self.assertTrue(any("Слово: с*б*ка" in str(call) for call in calls))
        self.assertTrue(any("Попыток осталось 5" in str(call) for call in calls))

        self.assertTrue(any("Использованные буквы:" in str(call) for call in calls))
        
        self.assertTrue(any("друг человека" in str(call) for call in calls))

    @patch('os.system')
    @patch('builtins.print')
    def test_get_game_stat_no_hint(self, mock_print, mock_system):
        ui = GameUI()
        
        mock_game = MagicMock()
        mock_game.get_picture_stage.return_value = 1
        mock_game.get_category.return_value = "профессии"
        mock_game.get_cur_state_word.return_value = "вр_ч"
        mock_game.get_attemps.return_value = 8
        mock_game.get_prev_letters.return_value = ["в", "р", "ч"]
        mock_game.get_is_hint_active.return_value = False
        mock_game.get_hint.return_value = "лечит людей"
        
        ui.get_game_stat(mock_game)

        hint_calls = [call for call in mock_print.call_args_list if "лечит людей" in str(call)]
        self.assertEqual(len(hint_calls), 0)