import argparse

from file_manager import Input, Output
from generator import Generator
from maze import Maze
from solver import Solver
from maze_render import UnicodeRender


def main() -> None:
    REQUIRED_GENERATE_ARGS = ["algorithm", "width", "height"]
    USAGE_GENERATE = "Использование: python main.py generate --algorithm=(dfs, prim) --width=(int) --height=(int)"

    REQUIRED_SOLVE_ARGS = ["algorithm", "file", "start", "end"]
    USAGE_SOLVE = "Использование: python main.py solve --algorithm=(dijkstra, astar) --file=(file) --start=(int,int) --end=(int,int)"

    parser = argparse.ArgumentParser(description="Обработка аргументов.")

    parser.add_argument(
        "task_type", type=str, help="Тип решаемой задачи", choices=["generate", "solve"]
    )
    parser.add_argument("--algorithm", type=str, help="Второе слово")

    parser.add_argument("--width", type=int, help="Ширина лабиринта", default=None)
    parser.add_argument("--height", type=int, help="Длина лабиринта", default=None)
    parser.add_argument(
        "--terrain",
        action='store_true',
        help="Различные поверхности",
        default=False,
    )

    parser.add_argument(
        "--start", type=str, help="Начальная точка маршрута", default=None
    )
    parser.add_argument("--end", type=str, help="Конечная точка маршрута", default=None)
    parser.add_argument(
        "--file", type=str, help="Файл с описанием лабиринта", default=None
    )

    parser.add_argument(
        "--output", type=str, help="Путь для сохранения лабиринта", default=None
    )
    parser.add_argument(
        "--unicode",
        action='store_true',
        help="Отрисовка в формате unicode символов",
        default=False,
    )

    args = parser.parse_args()

    if args.task_type == "generate":
        if validate_arguments(args, REQUIRED_GENERATE_ARGS, USAGE_GENERATE):
            handler_generate(args)

    elif args.task_type == "solve":
        if validate_arguments(args, REQUIRED_SOLVE_ARGS, USAGE_SOLVE):
            handler_solve(args)


def validate_arguments(args, required_args, usage) -> bool:
    missing = [word for word in required_args if not getattr(args, word)]
    if missing:
        print(f"Отсутствуют обязательные аргументы {', '.join(missing)}")
        print(usage)
        return False
    return True


def handler_generate(args):
    try:
        maze: Maze = Generator.generate(
            args.width, args.height, args.algorithm, args.terrain
        )

        handle_output(maze, args.unicode, args.output)
    except Exception as e:
        print(e)
        return


def handler_solve(args):
    try:
        maze: Maze = Input.input_from_file(args.file)

        maze_solver = Solver(maze, args.start, args.end, args.algorithm)
        success = maze_solver.execute()
        if not success:
            print("Невозможно найти маршрут")

        handle_output(maze, args.unicode, args.output)
    except Exception as e:
        print(e)
        return


def handle_output(maze: Maze, unicode=False, file_name=None) -> None:
    if unicode:
        UnicodeRender.render(maze)

    if file_name:
        Output.file_print(maze, file_name)
    else:
        Output.cl_print(maze)


if __name__ == "__main__":
    main()
