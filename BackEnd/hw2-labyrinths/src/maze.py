from cell import Cell, CellType
from path import Path

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._map = [[Cell(CellType.WALL) for _ in range(self.width)] for _ in range(self.height)]

    #Для проходимой части лабиринта
    def in_maze(self, x, y):
        return 0 < x < self.width-1 and 0 < y < self.height-1
    
    def set_cell(self, x, y, type: CellType):
        if self.in_maze(x, y):
            self._map[y][x] = Cell(type)

    def get_cell(self, x, y):
        return self._map[y][x]

    def is_cell_possible(self, x, y) -> bool:
        if self.in_maze(x, y) and \
            self._map[y][x].cost != float('inf'):
            return True
        return False
    
    def get_neighbours(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x, y = cell
        neighbors = []
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self.is_cell_possible(nx, ny)):
                neighbors.append((nx, ny))
        
        return neighbors

    def mark_path_to_maze(self, path: Path) -> None:
        for x, y in path.ready_path:
            self.set_cell(x, y, CellType.PATH)
        self.set_cell(path.start[0], path.start[1], CellType.START)
        self.set_cell(path.end[0], path.end[1], CellType.END)

    def to_unicode_converse(self):
        wall_map = self._get_unicode_map()
        self._apply_unicode_wall(wall_map)

    def _apply_unicode_wall(self, wall_map):
        unicode_chars = {
            (0,0,0,0): " ", (1,0,0,0): "╵", (0,1,0,0): "╶", (0,0,1,0): "╷", (0,0,0,1): "╴",
            (0,0,1,1): "┐", (0,1,1,0): "┌", (1,0,0,1): "┘", (1,1,0,0): "└",
            (1,1,1,0): "├", (1,0,1,1): "┤", (1,1,0,1): "┴", (0,1,1,1): "┬",
            (1,0,1,0): "│", (0,1,0,1):"─", (1,1,1,1): "┼"
        }
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y).type == CellType.WALL:
                    # У display есть setter, присвоить не unicode нельзя
                    # Cм. cell.py
                    self.get_cell(x, y).display = unicode_chars[wall_map[y][x]]


    def _get_unicode_map(self):
        DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        wall_map = []
        # Верх Право Низ Лево
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Для каждой клетки набираем список из 0 1
                # Далее этот список будет преобразован в юникод символы
                symb = []
                for dx, dy in DIRECTIONS: #Важен порядок добавления 1 или 0 в symb
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.get_cell(x, y).type == CellType.WALL and\
                         self.get_cell(nx, ny).type == CellType.WALL:
                            symb.append(1)
                            continue
                    symb.append(0)
                row.append(tuple(symb))
            wall_map.append(row)
        return wall_map