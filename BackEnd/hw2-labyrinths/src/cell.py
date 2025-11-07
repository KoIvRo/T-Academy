from enum import Enum


class CellType(Enum):
    START = ("O", 0)
    END = ("X", 1)
    WALL = ("#", float('inf'))
    SPACE = (" ", 1)
    PATH = (".", 1)
    SWAMP = ("~", 3)
    SAND = ("&", 2)
    COIN = ("+", -1)


class Cell:
    def __init__(self, cell_type: CellType):
        self.type = cell_type
        self._display = cell_type.value[0]
        self._cost = cell_type.value[1]
    
    @property
    def cost(self):
        return self._cost
    
    @property
    def display(self):
        return self._display
    
    @display.setter
    def display(self, char: str):
        if self.type == CellType.WALL and char in " ╵╶╷╴┐┌┘└├┤┴┬│─┼":
            self._display= char
            return
        raise ValueError(f"Неверное присвоение отображения символа {char}")