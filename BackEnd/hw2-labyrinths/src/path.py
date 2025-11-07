class Path:
    def __init__(self, path: list, start: tuple, end: tuple):
        self.ready_path = path
        self.start = start
        self.end = end

    @staticmethod
    def collect_path(start, end, previous: dict[tuple[int, int], tuple[int, int]]) -> list:
        path = []
        current = end

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        return path