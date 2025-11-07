class MainGame: # Класс для освновной логики игры, в нем 2 важные
    def __init__(self, word, hint, category, attemps, max_picture_stage):
        self._word = word
        self._hint = hint
        self._category = category
        self._attemps = attemps
        self._cur_state_word = ["*"] * len(word)
        self._is_win = False
        self._prev_letters = set()
        self._picture_stage = 0
        self._max_picture_stage = max_picture_stage
        self._is_hint_active = False


    def guess_letter(self):
        letter = input("Введите букву (что бы взять подсказку введите ?): ").strip().lower()

        while True:# Проверка ввода буквы
            if letter == "?" and not self.get_is_hint_active():
                self.set_is_hint_active(True)
                break
            elif letter == "?" and self.get_is_hint_active():
                print("Вы уже брали подсказку")
            elif len(letter) != 1:
                print("Одну букву")
            elif not letter.isalpha():
                print("Только буквы")
            elif letter in self.get_prev_letters():
                print("Буква уже была использована")
            else:
                break
            letter = input("Введите букву (что бы взять подсказку введите ?): ").strip().lower()

        #пропускаем обновление слова, переходим к новой игровой итерации
        if letter == "?":
            return

        #обновление слова
        is_guessed = False
        for ind in range(len(self.get_word())):

            if self.get_word()[ind] == letter and letter != self.get_cur_state_word()[ind]:
                self.set_cur_state_word(ind, letter)
                is_guessed = True

        if not is_guessed:
            self.dec_attemps()

        self.add_prev_letter(letter)

        if "*" not in self.get_cur_state_word():
            self.set_is_win(True)

    def status_check(self):
        if self.get_is_win() == True:
            print(f"Вы победили, слово {self.get_word()}")
        else:
            print(f"Попытки закончились\nВы програли, слово {self.get_word()}")
    
    #getter и setter
    def get_word(self):
        return self._word
    
    def get_hint(self):
        return self._hint
    
    def get_category(self):
        return self._category
    
    def get_attemps(self):
        return self._attemps
    
    def up_picture_stage(self):
        self._picture_stage = min(self.get_max_picture_stage() - 1, self.get_picture_stage() + 1)

    def dec_attemps(self):
        self._attemps -= 1
        self.up_picture_stage()

    def get_max_picture_stage(self):
        return self._max_picture_stage

    def get_cur_state_word(self):
        return "".join(self._cur_state_word)

    def set_cur_state_word(self, ind, letter):
        self._cur_state_word[ind] = letter
    
    def get_prev_letters(self):
        return ", ".join(list(self._prev_letters))
    
    def add_prev_letter(self, letters):
        self._prev_letters.add(letters)

    def set_is_win(self, state):
        self._is_win = state

    def get_is_win(self):
        return self._is_win
    
    def get_picture_stage(self):
        return self._picture_stage
    
    def get_is_hint_active(self):
        return self._is_hint_active
    
    def set_is_hint_active(self, state):
        self._is_hint_active = state