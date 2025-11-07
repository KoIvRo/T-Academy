class MainGame:
    def __init__(self, word, hint, category, tuple_attempts_and_sub_attemps):
        self._word = word
        self._hint = hint
        self._category = category
        self._attempts_count = tuple_attempts_and_sub_attemps[0]
        self._sub_attempts_tuple = tuple_attempts_and_sub_attemps[1]
        self._cur_state_word = ["*"] * len(word)
        self._is_win = False
        self._prev_letters = set()
        self._is_hint_active = False

    def guess_letter(self):
        letter = self._valid_input()

        if letter == "?":
            return
        
        if letter == "-":
            self._guess_word()
            return

        self._process_guess_letter(letter)

    def game_is_active(self):
        if (self._attempts_count > 0 and "*" in self._cur_state_word) and not self._is_win:
            return True
        else:
            if self._attempts_count > 0:
                self._is_win = True
            return False

    def get_game_stat(self):
        return {
            "word": self._word,
            "category": self._category,
            "cur_word": ''.join(self._cur_state_word),
            "tuple_attempts_and_sub_attemps": (self._attempts_count, self._sub_attempts_tuple),
            "letters": ', '.join(self._prev_letters),
            "hint": self._hint if self._is_hint_active else None,
            "state": self._is_win
        }
    
    def _process_guess_letter(self, letter):
        is_guessed = False
        for ind in range(len(self._word)):

            if self._word[ind] == letter and letter != self._cur_state_word[ind]:
                self._cur_state_word[ind] = letter
                is_guessed = True

        if not is_guessed:
            self._attempts_count -= 1
    
    def _guess_word(self):
        print("У вас будет одна попытка!")

        while True:
            check = input("Вы уверены[y, n]?: ").strip().lower()
            if check == "y" or check == "n":
                break

        if check == "y":
            word = input("Введите слово: ").strip().lower().replace("ё", "е")
            if word == self._word:
                self._is_win = True
            else:
                self._attempts_count = 0
    
    def _valid_input(self):
        print("Что бы взять подсказку введите ?") 
        print("Если вы готовы назвать слово введите -")
        while True:
            letter = input("Введите букву: ").strip().lower()
            if letter == "-":
                return letter
            if letter == "?" and not self._is_hint_active:
                self._is_hint_active = True
                return letter
            elif letter == "?" and self._is_hint_active:
                print("Вы уже брали подсказку")
                continue
            elif len(letter) != 1:
                print("Одну букву")
                continue
            elif not letter.isalpha() or letter not in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                print("Только русские буквы")
                continue
            elif letter in self._prev_letters:
                print("Буква уже была использована")
                continue
            self._prev_letters.add(letter)
            return letter