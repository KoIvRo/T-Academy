import unittest
from unittest.mock import patch, MagicMock
import io

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.mode import not_interactive_mode, interactive_mode


class TestNotInteractiveMode(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_not_interactive_mode_pos(self, mock_stdout):
        not_interactive_mode("а", "а")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "а;POS\n")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_not_interactive_mode_neg(self, mock_stdout):
        not_interactive_mode("а", "б")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "*;NEG\n")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_not_interactive_mode_pos_word_check(self, mock_stdout):
        not_interactive_mode("абвгд", "бвгад")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "****д;NEG\n")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_not_interactive_mode_pos_registr_check(self, mock_stdout):
        not_interactive_mode("А", "а")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "а;POS\n")

    def test_not_interactive_mode_invalid_input(self):        
        with self.assertRaises(ValueError) as context:
            not_interactive_mode("1", "1")
        self.assertEqual(str(context.exception), "Ввод должен содержать только буквы")
    
    def test_not_interactive_mode_diffirent_len_input(self):
        with self.assertRaises(ValueError) as context:
            not_interactive_mode("абв", "абвг")
        self.assertEqual(str(context.exception), "Слова должны быть одинковой длины")


class TestInteractiveMode(unittest.TestCase):
    @patch('src.mode.MainGame')
    @patch('src.mode.GameUI')
    @patch('src.mode.PrepareGame')
    def test_interactive_mode_win(self, mock_prepare, mock_ui, mock_game):
        mock_prepare.word_choice.return_value = ("кот", "word", "hint")
        mock_prepare.difficult_choice.return_value = 7

        mock_ui_instance = MagicMock()
        mock_ui.return_value = mock_ui_instance

        mock_game_instance = MagicMock()
        mock_game.return_value = mock_game_instance
        mock_game_instance.game_is_active.side_effect = [True, True, False]
        mock_game_instance.get_game_stat.return_value = {"stat": "dummy"}

        interactive_mode()

        self.assertEqual(mock_game_instance.guess_letter.call_count, 2)
        self.assertEqual(mock_ui_instance.print_game_stat.call_count, 2)
        mock_ui_instance.print_final_stat.assert_called_once_with({"stat": "dummy"})

    @patch('src.mode.MainGame')
    @patch('src.mode.GameUI')
    @patch('src.mode.PrepareGame')
    def test_interactive_mode_lose_condition(self, mock_prepare, mock_ui, mock_game):
        mock_prepare.word_choice.return_value = ("кот", "word", "hint")
        mock_prepare.difficult_choice.return_value = 3

        mock_ui_instance = MagicMock()
        mock_ui.return_value = mock_ui_instance

        mock_game_instance = MagicMock()
        mock_game.return_value = mock_game_instance

        mock_game_instance.game_is_active.side_effect = [True, True, True, False]
        mock_game_instance.get_game_stat.return_value = {"stat": "dummy"}

        interactive_mode()

        self.assertEqual(mock_game_instance.guess_letter.call_count, 3)
        self.assertEqual(mock_ui_instance.print_game_stat.call_count, 3)
        mock_ui_instance.print_final_stat.assert_called_once_with({"stat": "dummy"})