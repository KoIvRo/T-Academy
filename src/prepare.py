import random

class PrepareGame:
    # Категории и списки можно добавлять сюда, в коде ничего больше меня не нужно при изменении этого словаря
    _dictionary_category = {
        "профессии": [("врач", "он лечит людей"), ("полицейский", "он ищет преступников"), ("программист", "он пишет программы")],
        "игры": [("баскетбол", "в этой игре бросают мяч в корзину"), ("футбол", "в эту игру играют ногами"), ("хоккей", "игра идет на льду")],
        "животные": [("зебра", "животное в черно-белую полоску"), ("жираф", "у него длинная шея"), ("собака", "это животное считается другом человека")]
    }

    # Точно также при изменении параметров сложности другие изменения в коде не требуются
    _dictionary_difficults = {
        "легкий": 9,
        "средний": 8,
        "тяжелый": 7
    }

    @staticmethod
    def word_choice():
        print("Можно выбрать категорию слов, пропуска выбора ENTER")

        category = input(f"Выберите категорию слов {PrepareGame.get_category()}: ").strip().lower()
        while category and category not in PrepareGame.get_category():
            print("Такой категории нет, попробуйте еще раз")
            category = input(f"Выберите категорию слов {PrepareGame.get_category()}: ").strip().lower()

        # Рандом(пользователь не ввел ничего)
        if not category:
            category = random.choice(list(PrepareGame._dictionary_category))

        word, hint = random.choice(PrepareGame._dictionary_category[category])
        return category, word, hint

    @staticmethod
    def difficult_choice():
        print("Можно выбрать уровень сложности (рекомендовано тяжелый), для пропуска выбора ENTER")
        print("Легкий 9 попыток, Средний 8 попыток, Тяжелый 7 попыток")

        difficult = input(f"Выберите уровень сложности {PrepareGame.get_difficults()}: ").strip().lower().replace("ё", 'е')
        while difficult and difficult not in PrepareGame.get_difficults():
            print("Такого уровня сложности нет, попробуйте еще раз")
            difficult = input(f"Выберите уровень сложности {PrepareGame.get_difficults()}: ").strip().lower().replace("ё", 'е')

        # Рандом(пользователь не ввел ничего)
        if not difficult:
            difficult = random.choice(list(PrepareGame._dictionary_difficults))

        return PrepareGame._dictionary_difficults[difficult]
    
    # Геттеры
    @staticmethod
    def get_category():
        return list(PrepareGame._dictionary_category)

    @staticmethod
    def get_difficults():
        return list(PrepareGame._dictionary_difficults)