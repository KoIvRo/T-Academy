import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from prepare import PrepareGame
from game import MainGame
from UI import GameUI

def not_interactive_mode(hidden_word, visible_word):
    if not (hidden_word.isalpha() and visible_word.isalpha()):
        raise ValueError("Ввод должен содержать только буквы")
    if (len(hidden_word) != len(visible_word)):
        raise ValueError("Слова должны быть одинковой длины")
    hidden_word, visible_word = hidden_word.lower(), visible_word.lower()
    is_win = "POS"
    for ind in range(len(hidden_word)):
        if hidden_word[ind] == visible_word[ind]:
            print(hidden_word[ind], end = "")
        else:
            is_win = "NEG"
            print("*", end = "")
    print(f";{is_win}")

def interactive_mode():
    category, word, hint = PrepareGame.word_choice()
    tuple_attempts_and_sub_attemps = PrepareGame.difficult_choice()

    game_ui = GameUI()
    game = MainGame(word, hint, category, tuple_attempts_and_sub_attemps)

    while game.game_is_active():
        game_stat = game.get_game_stat()
        game_ui.print_game_stat(game_stat)

        game.guess_letter()
    
    game_stat = game.get_game_stat()
    game_ui.print_final_stat(game_stat)