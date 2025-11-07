import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from game import MainGame

class TestGame(unittest.TestCase):
    @patch('builtins.input', return_value='к')
    @patch('builtins.print')
    def test_guess_letter_correct(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        
        game.guess_letter()
        
        self.assertEqual(game.get_cur_state_word(), "к**")
        self.assertEqual(game.get_attemps(), 5)
        self.assertEqual(game.get_prev_letters(), "к")
        self.assertFalse(game.get_is_win())

    @patch('builtins.input', return_value='x')
    @patch('builtins.print')
    def test_guess_letter_incorrect(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        
        game.guess_letter()
        
        self.assertEqual(game.get_cur_state_word(), "***")
        self.assertEqual(game.get_attemps(), 4)
        self.assertEqual(game.get_prev_letters(), "x")
        self.assertEqual(game.get_picture_stage(), 1)
        self.assertFalse(game.get_is_win())

    @patch('builtins.input', side_effect=['?', 'к'])
    @patch('builtins.print')
    def test_guess_letter_hint_first_time(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        
        game.guess_letter()
        
        self.assertTrue(game.get_is_hint_active())
        self.assertEqual(game.get_attemps(), 5)
        self.assertEqual(game.get_prev_letters(), "")
        self.assertEqual(game.get_cur_state_word(), "***")

    @patch('builtins.input', side_effect=['?', '?', 'к'])
    @patch('builtins.print')
    def test_guess_letter_hint_second_time(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        game.set_is_hint_active(True)
        
        game.guess_letter()
        mock_print.assert_any_call("Вы уже брали подсказку")
        self.assertTrue(game.get_is_hint_active())

    @patch('builtins.input', side_effect=['кк', 'к'])
    @patch('builtins.print')
    def test_guess_letter_invalid_length(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        
        game.guess_letter()
        
        mock_print.assert_any_call("Одну букву")
        self.assertEqual(game.get_cur_state_word(), "к**")

    @patch('builtins.input', side_effect=['1', 'к'])
    @patch('builtins.print')
    def test_guess_letter_non_alpha(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        
        game.guess_letter()
        
        mock_print.assert_any_call("Только буквы")
        self.assertEqual(game.get_cur_state_word(), "к**")

    @patch('builtins.input', side_effect=['к', 'к', 'о'])
    @patch('builtins.print')
    def test_guess_letter_repeated_letter(self, mock_print, mock_input):
        game = MainGame("кот", "hint", "category", 5, 7)
        
        game.guess_letter()
        game.guess_letter()
        
        mock_print.assert_any_call("Буква уже была использована")
        self.assertEqual(game.get_cur_state_word(), "ко*")
        self.assertEqual(game.get_prev_letters(), "к, о")

    def test_win_condition(self):
        game = MainGame("кот", "hint", "category", 5, 7)
        for letter in "кот":
            game.set_cur_state_word = MagicMock()
            game.add_prev_letter(letter)
            game._cur_state_word = list("кот")
        
        game._cur_state_word = list("кот")
        self.assertTrue("*" not in game.get_cur_state_word())
        game.set_is_win(True)
        
        self.assertTrue(game.get_is_win())

    @patch('builtins.print')
    def test_status_check_win(self, mock_print):
        game = MainGame("кот", "hint", "category", 5, 7)
        game.set_is_win(True)
        
        game.status_check()
        
        mock_print.assert_any_call("Вы победили, слово кот")

    @patch('builtins.print')
    def test_status_check_lose(self, mock_print):
        game = MainGame("кот", "hint", "category", 0, 7)
        game.set_is_win(False)
        
        game.status_check()
        calls = mock_print.call_args_list
        self.assertTrue(any("Попытки закончились" in str(call) for call in calls))
        self.assertTrue(any("Вы програли, слово кот" in str(call) for call in calls))

    def test_picture_stage_limits(self):
        game = MainGame("кот", "hint", "category", 5, 3)

        for _ in range(10):
            game.up_picture_stage()
        
        self.assertEqual(game.get_picture_stage(), 2)