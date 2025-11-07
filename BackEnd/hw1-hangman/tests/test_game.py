import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.game import MainGame

class TestGame(unittest.TestCase):
    @patch('builtins.input', return_value='к')
    @patch('builtins.print')
    def test_guess_letter_correct(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        stat = game.get_game_stat()
        self.assertEqual(stat["cur_word"], "к**")
        self.assertEqual(stat["tuple_attempts_and_sub_attemps"][0], 5)
        self.assertIn('к', stat["letters"])
        self.assertFalse(stat["state"])

    @patch('builtins.input', return_value='х')
    @patch('builtins.print')
    def test_guess_letter_incorrect(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        stat = game.get_game_stat()
        self.assertEqual(stat["cur_word"], "***")
        self.assertEqual(stat["tuple_attempts_and_sub_attemps"][0], 4)
        self.assertIn('х', stat["letters"])
        self.assertFalse(stat["state"])

    @patch('builtins.input', side_effect=['?', 'к'])
    @patch('builtins.print')
    def test_guess_letter_hint_first_time(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        stat = game.get_game_stat()
        self.assertEqual(stat["hint"], "hint")
        self.assertEqual(stat["tuple_attempts_and_sub_attemps"][0], 5)
        self.assertEqual(stat["letters"], '')
        self.assertEqual(stat["cur_word"], "***")

    @patch('builtins.input', side_effect=['?', '?', 'к'])
    @patch('builtins.print')
    def test_guess_letter_hint_second_time(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        game._is_hint_active = True
        
        game.guess_letter()
        
        mock_print.assert_any_call("Вы уже брали подсказку")
        stat = game.get_game_stat()
        self.assertEqual(stat["hint"], "hint")

    @patch('builtins.input', side_effect=['кк', 'к'])
    @patch('builtins.print')
    def test_guess_letter_invalid_length(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        mock_print.assert_any_call("Одну букву")
        stat = game.get_game_stat()
        self.assertEqual(stat["cur_word"], "к**")

    @patch('builtins.input', side_effect=['1', 'к'])
    @patch('builtins.print')
    def test_guess_letter_non_alpha(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        mock_print.assert_any_call("Только русские буквы")
        stat = game.get_game_stat()
        self.assertEqual(stat["cur_word"], "к**")

    @patch('builtins.input', side_effect=['1', 'r', "к"])
    @patch('builtins.print')
    def test_guess_letter_non_russians(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        mock_print.assert_any_call("Только русские буквы")
        stat = game.get_game_stat()
        self.assertEqual(stat["cur_word"], "к**")

    @patch('builtins.input', side_effect=['к', 'к', 'о'])
    @patch('builtins.print')
    def test_guess_letter_repeated_letter(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        game.guess_letter()
        
        mock_print.assert_any_call("Буква уже была использована")
        stat = game.get_game_stat()
        self.assertEqual(stat["cur_word"], "ко*")
        self.assertIn('к', stat["letters"])
        self.assertIn('о', stat["letters"])

    def test_win_condition(self):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        game._prev_letters = set("кот")
        game._cur_state_word = list("кот")
        
        self.assertFalse("*" in game.get_game_stat()["cur_word"])
        game._is_win = True
        
        self.assertTrue(game.get_game_stat()["state"])

    @patch('builtins.print')
    def test_status_check_win(self, mock_print):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        game._is_win = True
        
        self.assertFalse(game.game_is_active(), False)
        self.assertTrue(game._is_win, True)

    @patch('builtins.print')
    def test_status_check_lose(self, mock_print):
        game = MainGame("кот", "hint", "category", (0, [3, 4, 5]))
        game._is_win = False
        
        self.assertFalse(game.game_is_active(), False)
        self.assertFalse(game._is_win, False)

    def test_game_is_active_win(self):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        game._cur_state_word = list("кот")
        
        result = game.game_is_active()
        
        self.assertTrue(game.get_game_stat()["state"])
        self.assertFalse(result)

    def test_game_is_active_lose(self):
        game = MainGame("кот", "hint", "category", (0, [3, 4, 5]))
        
        result = game.game_is_active()
        
        self.assertFalse(game.get_game_stat()["state"])
        self.assertFalse(result)

    def test_game_is_active_continue(self):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        result = game.game_is_active()
        
        self.assertTrue(result)
        self.assertFalse(game.get_game_stat()["state"])

    @patch('builtins.input', side_effect=['y', 'кот'])
    @patch('builtins.print')
    def test_guess_word_correct(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game._guess_word()
        
        self.assertTrue(game.get_game_stat()["state"])

    @patch('builtins.input', side_effect=['y', 'собака'])
    @patch('builtins.print')
    def test_guess_word_incorrect(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game._guess_word()
        
        stat = game.get_game_stat()
        self.assertFalse(stat["state"])
        self.assertEqual(stat["tuple_attempts_and_sub_attemps"][0], 0)

    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_guess_word_cancel(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game._guess_word()
        
        stat = game.get_game_stat()
        self.assertFalse(stat["state"])
        self.assertEqual(stat["tuple_attempts_and_sub_attemps"][0], 5)

    @patch('builtins.input', side_effect=['-', 'y', 'кот'])
    @patch('builtins.print')
    def test_guess_letter_with_word_guess(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", (5, [3, 4, 5]))
        
        game.guess_letter()
        
        self.assertTrue(game.get_game_stat()["state"])