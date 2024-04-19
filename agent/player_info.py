from typing import List, Literal

from .position import Position

type ArmorKind = Literal[
    "NO_ARMOR",
    "PRIMARY_ARMOR",
    "PREMIUM_ARMOR",
]

type FirearmKind = Literal[
    "S686",
    "M16",
    "AWM",
    "VECTOR",
]

type ItemKind = Literal[
    "BANDAGE",
    "FIRST_AID",
    "BULLET",
    "GRENADE",
]


class Item:
    def __init__(self, kind: ItemKind, count: int):
        self.kind = kind
        self.count = count


class PlayerInfo:
    def __init__(
        self,
        id: int,
        armor: ArmorKind,
        health: int,
        speed: float,
        firearm: FirearmKind,
        range: float,
        position: Position[float],
        inventory: List[Item],
    ):
        self.id = id
        self.armor = armor
        self.health = health
        self.speed = speed
        self.firearm = firearm
        self.range = range
        self.position = position
        self.inventory = inventory

    def __str__(self) -> str:
        return f"PlayerInfo{{id: {self.id}, armor: {self.armor}, health: {self.health}, speed: {self.speed}, firearm: {self.firearm}, range: {self.range}, position: {self.position}, inventory: {self.inventory}}}"
