import unittest
from unittest.mock import patch
from prepare import PrepareGame

class TestPrepare(unittest.TestCase):

    def test_get_category(self):        
        categories = PrepareGame.get_category()
        expected_categories = ["профессии", "игры", "животные"]
        
        self.assertEqual(sorted(categories), sorted(expected_categories))

    def test_get_difficults(self):
        difficults = PrepareGame.get_difficults()
        expected_difficults = ["легкий", "средний", "тяжелый"]
        
        self.assertEqual(sorted(difficults), sorted(expected_difficults))

    @patch('builtins.input', side_effect=['1', 'профессии'])
    @patch('builtins.print')
    def test_word_choice_valid_category(self, mock_print, mock_input):
        with patch('random.choice') as mock_random_choice:
            mock_random_choice.return_value = ("врач", "он лечит людей")
            
            category, word, hint = PrepareGame.word_choice()
            
            self.assertEqual(category, "профессии")
            self.assertEqual(word, "врач")
            self.assertEqual(hint, "он лечит людей")


    @patch('builtins.input', side_effect=['', ''])
    @patch('builtins.print')
    def test_word_choice_random_category(self, mock_print, mock_input):
        with patch('random.choice') as mock_random_choice:
            mock_random_choice.side_effect = ['животные', ('зебра', 'животное в полоску')]
            
            category, word, hint = PrepareGame.word_choice()
            
            self.assertEqual(category, "животные")
            self.assertEqual(word, "зебра")
            mock_random_choice.assert_called()


    @patch('builtins.input', side_effect=['несуществующая', 'профессии'])
    @patch('builtins.print')
    def test_word_choice_invalid_then_valid_category(self, mock_print, mock_input):
        with patch('random.choice') as mock_random_choice:
            mock_random_choice.return_value = ("полицейский", "он ищет преступников")
            
            category, word, hint = PrepareGame.word_choice()
            
            self.assertEqual(category, "профессии")
            self.assertEqual(word, "полицейский")
            self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['легкий'])
    @patch('builtins.print')
    def test_difficult_choice_valid_difficult(self, mock_print, mock_input):
        attempts = PrepareGame.difficult_choice()
        
        self.assertEqual(attempts, 9)


    @patch('builtins.input', side_effect=['', ''])
    @patch('builtins.print')
    def test_difficult_choice_random_difficult(self, mock_print, mock_input):
        with patch('random.choice') as mock_random_choice:
            mock_random_choice.return_value = 'средний'
            
            attempts = PrepareGame.difficult_choice()
            
            self.assertEqual(attempts, 8)
            mock_random_choice.assert_called_once()

    @patch('builtins.input', side_effect=['очень сложный', 'тяжелый'])
    @patch('builtins.print')
    def test_difficult_choice_invalid_then_valid(self, mock_print, mock_input):
        
        attempts = PrepareGame.difficult_choice()
        
        self.assertEqual(attempts, 7)
        self.assertEqual(mock_input.call_count, 2)