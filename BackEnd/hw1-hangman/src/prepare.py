import random

class PrepareGame:
    _dictionary_category = {
        "профессии": [("врач", "Он лечит людей"), ("полицейский", "Он ищет преступников"), ("программист", "Он пишет программы")],
        "игры": [("баскетбол", "В этой игре бросают мяч в корзину"), ("футбол", "В эту игру играют ногами"), ("хоккей", "Игра идет на льду")],
        "животные": [("зебра", "Животное в черно-белую полоску"), ("жираф", "У него длинная шея"), ("собака", "Это животное считается другом человека")]
    }


    # Количество цифр для перехода на новую стадию рисунка не должно превышать количество стадий!!!
    _dictionary_difficults = {
        "легкий": (10, (9, 6, 4, 2, 1, 0)),
        "средний": (8, (7, 5, 4, 2, 1, 0)),
        "тяжелый": (7, (6, 5, 3, 2, 1, 0))
    }

    @staticmethod
    def word_choice():
        print("Можно выбрать категорию слов, пропуска выбора ENTER")

        category = input(f"Выберите категорию слов {list(PrepareGame._dictionary_category)}: ").strip().lower()
        while category and category not in PrepareGame._dictionary_category:
            print("Такой категории нет, попробуйте еще раз")
            category = input(f"Выберите категорию слов {list(PrepareGame._dictionary_category)}: ").strip().lower()

        if not category:
            category = random.choice(list(PrepareGame._dictionary_category))

        word, hint = random.choice(PrepareGame._dictionary_category[category])
        return category, word, hint

    @staticmethod
    def difficult_choice():
        print("Можно выбрать уровень сложности (рекомендовано тяжелый), для пропуска выбора ENTER")
        print("Легкий 10 попыток, Средний 8 попыток, Тяжелый 7 попыток")

        difficult = input(f"Выберите уровень сложности {list(PrepareGame._dictionary_difficults)}: ").strip().lower().replace("ё", 'е')
        while difficult and difficult not in PrepareGame._dictionary_difficults:
            print("Такого уровня сложности нет, попробуйте еще раз")
            difficult = input(f"Выберите уровень сложности {list(PrepareGame._dictionary_difficults)}: ").strip().lower().replace("ё", 'е')

        if not difficult:
            difficult = random.choice(list(PrepareGame._dictionary_difficults))

        return PrepareGame._dictionary_difficults[difficult]