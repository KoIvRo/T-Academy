import unittest
from unittest.mock import patch
from src.main import main
import io

class TestMain(unittest.TestCase):

    @patch('src.main.not_interactive_mode')
    def test_both_arguments_calls_not_interactive(self, mock_not_interactive):
        test_args = ['main.py', 'а', 'б']
        with patch('sys.argv', test_args):
            main()
        mock_not_interactive.assert_called_once_with('а', 'б')
    
    @patch('src.main.interactive_mode')
    def test_no_arguments_calls_interactive(self, mock_interactive):
        test_args = ['main.py']
        with patch('sys.argv', test_args):
            main()
        mock_interactive.assert_called_once()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.main.interactive_mode')
    @patch('src.main.not_interactive_mode')
    def test_only_one_argument_prints_1(self, mock_not_interactive, mock_interactive, mock_stdout):
        test_args = ['main.py', 'a']
        
        with patch('sys.argv', test_args):
            main()
        
        output = mock_stdout.getvalue()
        self.assertEqual(output, '1\n')

        mock_interactive.assert_not_called()
        mock_not_interactive.assert_not_called()