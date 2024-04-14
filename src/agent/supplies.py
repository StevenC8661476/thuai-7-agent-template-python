class Position:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

class Supply:
    def __init__(self, name: str, position: Position, numb: int):
        self.Name = name
        self.Position = position
        self.Numb = numb
