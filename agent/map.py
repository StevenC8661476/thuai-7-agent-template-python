class Position:
    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y


class Map:
    def __init__(self, length: int, walls: list[Position]):
        self.Length = length
        self.Walls = walls
