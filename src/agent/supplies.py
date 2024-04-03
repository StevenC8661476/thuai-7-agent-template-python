class Position:
    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y

class Supply:
    def __init__(self, name: str, position: Position):
        self.Name = name
        self.Position = position
