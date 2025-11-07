import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import io
from mode import not_interactive_mode, interactive_mode

class TetsNotInteractiveMode(unittest.TestCase):

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
        self.assertEqual(output, "абвгд;POS\n")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_not_interactive_mode_pos_registr_check(self, mock_stdout):
        not_interactive_mode("А", "а")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "а;POS\n")

    def test_not_interactive_mode_invalid_input(self):        
        with self.assertRaises(ValueError) as context:
            not_interactive_mode("1", "1")
        
        self.assertEqual(str(context.exception), "Ввод должен содержать только буквы")

        with self.assertRaises(ValueError) as context:
            not_interactive_mode("1", "1")
        
        self.assertEqual(str(context.exception), "Ввод должен содержать только буквы")

class TestInteractiveMode(unittest.TestCase):
    @patch('mode.MainGame')
    @patch('mode.GameUI')
    @patch('mode.PrepareGame')
    def test_interactive_mode_win(self, mock_prepare, mock_ui, mock_game):
        mock_prepare.word_choice.return_value = ("кот", "word", "hint")
        mock_prepare.difficult_choice.return_value = 7
        mock_ui_instance = MagicMock()
        mock_ui.return_value = mock_ui_instance
        mock_ui_instance.get_len_hangman_stage.return_value = 6
        
        mock_game_instance = MagicMock()
        mock_game.return_value = mock_game_instance
        mock_game_instance.get_is_win.side_effect = [False, False, True]
        mock_game_instance.get_attemps.return_value = 3
        
        interactive_mode()
        
        self.assertEqual(mock_game_instance.guess_letter.call_count, 2)
        mock_game_instance.status_check.assert_called_once()

    @patch('mode.MainGame')
    @patch('mode.GameUI')
    @patch('mode.PrepareGame')
    def test_interactive_mode_lose_condition(self, mock_prepare, mock_ui, mock_game):
        mock_prepare.word_choice.return_value = ("кот", "word", "hint")
        mock_prepare.difficult_choice.return_value = 3
        mock_ui_instance = MagicMock()
        mock_ui.return_value = mock_ui_instance
        mock_ui_instance.get_len_hangman_stage.return_value = 6
        
        mock_game_instance = MagicMock()
        mock_game.return_value = mock_game_instance
        mock_game_instance.get_is_win.return_value = False
        mock_game_instance.get_attemps.side_effect = [3, 2, 1, 0]
        
        interactive_mode()
        
        self.assertEqual(mock_game_instance.guess_letter.call_count, 3)
        mock_game_instance.status_check.assert_called_once()