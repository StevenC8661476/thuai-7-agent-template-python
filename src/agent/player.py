class Firearm:
    def __init__(self, name: str, distance: float):
        self.Name = name
        self.Distance = distance

class Position:
    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y

class Player:
    def __init__(self, playerId: int, armor: str, health: int, speed: float, firearm: Firearm, position: Position):
        self.PlayerId = playerId
        self.Armor = armor
        self.Health = health
        self.Speed = speed
        self.Firearm = firearm
        self.Position = position
