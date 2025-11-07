import os
class GameUI:
    def __init__(self):
        self._hangman_stage = [
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||
        | |/         ||
        | |          ||_
        | |          (   )
        | |           (__)
        | |
        | |
        | |
        | |
        | |
        | |
        | |
        | |
        | |
        ++++++++++++++++++++++
        """,
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||.-''.
        | |/         |/  _  \\
        | |          ||  `/,|
        | |          (\\`_.'
        | |                  
        | |                  
        | |                  
        | |                  
        | |                  
        | |                  
        | |                  
        | |                  
        | |                  
        | |                  
        ++++++++++++++++++++++
        """,
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||.-''.
        | |/         |/  _  \\
        | |          ||  `/,|
        | |          (\\`_.'
        | |         .-`--'.
        | |        /Y . . Y\\
        | |          |   |
        | |          | . |
        | |          |   |
        | |                   
        | |                   
        | |                   
        | |                   
        | |                   
        ++++++++++++++++++++++
        """,
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||.-''.
        | |/         |/  _  \\
        | |          ||  `/,|
        | |          (\\`_.'
        | |         .-`--'.
        | |        /Y . . Y\\
        | |       // |   |
        | |      //  | . |
        | |     ')   |   |
        | |                   
        | |                   
        | |                   
        | |                   
        | |                   
        ++++++++++++++++++++++
        """,
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||.-''.
        | |/         |/  _  \\
        | |          ||  `/,|
        | |          (\\`_.'
        | |         .-`--'.
        | |        /Y . . Y\\
        | |       // |   | \\
        | |      //  | . |  \\
        | |     ')   |   |   (`
        | |                   
        | |                   
        | |                   
        | |                   
        | |                   
        ++++++++++++++++++++++
        """,
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||.-''.
        | |/         |/  _  \\
        | |          ||  `/,|
        | |          (\\`_.'
        | |         .-`--'.
        | |        /Y . . Y\\
        | |       // |   | \\
        | |      //  | . |  \\
        | |     ')   |   |   (`
        | |          ||
        | |          ||
        | |          ||
        | |          ||
        | |         / |
        ++++++++++++++++++++++
        """,
        """
        ___________..________.
        | .__________))______|
        | | / /      ||
        | |/ /       ||
        | | /        ||.-''.
        | |/         |/  _  \\
        | |          ||  `/,|
        | |          (\\`_.'
        | |         .-`--'.
        | |        /Y . . Y\\
        | |       // |   | \\
        | |      //  | . |  \\
        | |     ')   |   |   (`
        | |          || ||
        | |          || ||
        | |          || ||
        | |          || ||
        | |         / | | \\
        ++++++++++++++++++++++
        """]

        self._current_stage = 0
        self._last_attempts = None
    
    def _update_stage_by_attemps(self, tuple_attempts_and_sub_attemps):
        if self._last_attempts is None:
            self._last_attempts = tuple_attempts_and_sub_attemps[0]
            return
        
        if tuple_attempts_and_sub_attemps[0] in tuple_attempts_and_sub_attemps[1] and self._last_attempts > tuple_attempts_and_sub_attemps[0]:
            if self._current_stage < len(self._hangman_stage):
                self._current_stage += 1
        
        self._last_attempts = tuple_attempts_and_sub_attemps[0]


    def print_game_stat(self, game_stat):
        os.system("cls")

        self._update_stage_by_attemps(game_stat['tuple_attempts_and_sub_attemps'])

        print(self._hangman_stage[self._current_stage])

        info_lines = [
            f"Категория: {game_stat['category']}",
            f"Слово: {game_stat['cur_word']}",
            f"Попыток осталось: {game_stat['tuple_attempts_and_sub_attemps'][0]}",
            f"Использованные буквы: {game_stat['letters']}"
        ]
        
        if game_stat['hint']:
            info_lines.append(f"Подсказка: {game_stat['hint']}")
        
        print("\n".join(info_lines))
    
    def print_final_stat(self, game_stat):
        os.system("cls")
        self._update_stage_by_attemps(game_stat['tuple_attempts_and_sub_attemps'])
        print(self._hangman_stage[self._current_stage])

        if game_stat["state"]:
            print(f"Вы победили, слово {game_stat['word']}")
        else:
            print(f"Вы програли, слово {game_stat['word']}")