from cell import CellType
from maze import Maze


class Output:
    @staticmethod
    def cl_print(maze) -> None:
        for y in range(maze.height):
            for x in range(maze.width):
                print(maze.get_cell(x, y).display, end="")
            print()

    @staticmethod
    def file_print(maze, file) -> None:
        with open(file, "w", encoding="utf-8") as f:
            for y in range(maze.height):
                f.writelines(maze.get_cell(x, y).display for x in range(maze.width))
                f.write("\n")


class Input:
    @staticmethod
    def input_from_file(filename: str) -> Maze:
        with open(filename, encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]

        if not lines:
            raise ValueError("Файл пуст")

        height = len(lines)
        width = len(lines[0])

        for line in lines:
            if len(line) != width:
                raise ValueError("На вход поступили строки разной длины")

        maze = Maze(width, height)

        for y in range(height):
            for x in range(width):
                cell_type = CellType.from_symbol(lines[y][x])

                if cell_type:
                    maze.set_cell(x, y, cell_type)
                else:
                    raise ValueError(
                        f"Пожалуйста проверьте ваш файл {x, y}\nДопустимые символы: #, ' ', &, ~"
                    )
        return maze
