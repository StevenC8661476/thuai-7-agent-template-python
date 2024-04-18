from typing import List


class Firearm:
    def __init__(self, name: str, distance: float):
        self.Name = name
        self.Distance = distance


class Position:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y


class Item:
    def __init__(self, name: str, num: int):
        self.Name = name
        self.Num = num


class Inventory:
    def __init__(self, supplies: List[Item]):
        self.Supplies = list(supplies)


class Player:
    def __init__(
        self,
        playerId: int,
        armor: str,
        health: int,
        speed: float,
        firearm: Firearm,
        position: Position,
        inventory: Inventory,
    ):
        self.PlayerId = playerId
        self.Armor = armor
        self.Health = health
        self.Speed = speed
        self.Firearm = firearm
        self.Position = position
        self.Inventory = inventory
