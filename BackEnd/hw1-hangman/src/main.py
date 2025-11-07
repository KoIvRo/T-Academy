import argparse
import os
import sys

# ВАЖНО!!!
# Добавляем путь к src, что бы при запуске тестов из tests находились модули из src
# По другому не работает
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from mode import not_interactive_mode, interactive_mode

def main() -> None:
    parser = argparse.ArgumentParser(description="Обработка слов для игры.")
    parser.add_argument("hidden_word", type=str, nargs="?", help="Первое слово (загадать)")
    parser.add_argument("visible_word", type=str, nargs="?", help="Второе слово (отгадать)")

    args = parser.parse_args()

    if args.hidden_word and args.visible_word:
        not_interactive_mode(args.hidden_word, args.visible_word)
    elif not args.hidden_word and not args.visible_word:
        interactive_mode()
    else:
        return

if __name__ == "__main__":
    main()