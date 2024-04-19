import asyncio
import logging
from typing import List, Literal, Optional

from . import messages
from .map import Map
from .player_info import FirearmKind, Item, ItemKind, PlayerInfo
from .position import Position
from .safe_zone import SafeZone
from .supply import Supply
from .websocket_client import WebsocketClient

type MedicineKind = Literal[
    "BANDAGE",
    "FIRST_AID",
]


class Agent:
    def __init__(self, token: str, loop_interval: float):
        self._loop_interval = loop_interval
        self._token = token

        self._all_player_info: Optional[List[PlayerInfo]] = None
        self._map: Optional[Map] = None
        self._supplies: Optional[List[Supply]] = None
        self._safe_zone: Optional[SafeZone] = None
        self._self_id: Optional[int] = None

        self._websocket_client = WebsocketClient("")  # Just a placeholder.
        self._task_list: List[asyncio.Task] = []

    def __str__(self) -> str:
        return f"Agent{{token: {self._token}}}"

    @property
    def all_player_info(self) -> Optional[List[PlayerInfo]]:
        return self._all_player_info

    @property
    def map(self) -> Optional[Map]:
        return self._map

    @property
    def supplies(self) -> Optional[List[Supply]]:
        return self._supplies

    @property
    def safe_zone(self) -> Optional[SafeZone]:
        return self._safe_zone

    @property
    def self_id(self) -> Optional[int]:
        return self._self_id

    @property
    def token(self) -> str:
        return self._token

    async def connect(self, server: str):
        self._websocket_client = WebsocketClient(server)
        self._websocket_client.register_message_handler(self._on_message)
        await self._websocket_client.run()

        self._task_list.append(asyncio.create_task(self._loop()))

    async def disconnect(self):
        for task in self._task_list:
            task.cancel()

        await self._websocket_client.stop()

    def is_game_ready(self) -> bool:
        return (
            self._all_player_info is not None
            and self._map is not None
            and self._supplies is not None
            and self._safe_zone is not None
            and self._self_id is not None
        )

    def abandon(self, item_kind: ItemKind, count: int):
        self._websocket_client.send(
            messages.PerformAbandonMessage(
                token=self._token,
                numb=count,
                target_supply=item_kind,
            )
        )

    def pick_up(self, item_kind: ItemKind, count: int, position: Position[float]):
        self._websocket_client.send(
            messages.PerformPickUpMessage(
                token=self._token,
                target_supply=item_kind,
                num=count,
                target_position=messages.Position(x=position.x, y=position.y),
            )
        )

    def switch_weapon(self, item_kind: FirearmKind):
        self._websocket_client.send(
            messages.PerformSwitchArmMessage(
                token=self._token,
                target_firearm=item_kind,
            )
        )

    def use_medicine(self, item_kind: MedicineKind):
        self._websocket_client.send(
            messages.PerformUseMedicineMessage(
                token=self._token,
                medicine_name=item_kind,
            )
        )

    def use_grenade(self, position: Position[float]):
        self._websocket_client.send(
            messages.PerformUseGrenadeMessage(
                token=self._token,
                target_position=messages.Position(x=position.x, y=position.y),
            )
        )

    def move(self, position: Position[float]):
        self._websocket_client.send(
            messages.PerformMoveMessage(
                token=self._token,
                destination=messages.Position(x=position.x, y=position.y),
            )
        )

    def stop(self):
        self._websocket_client.send(
            messages.PerformStopMessage(
                token=self._token,
            )
        )

    def attack(self, position: Position[float]):
        self._websocket_client.send(
            messages.PerformAttackMessage(
                token=self._token,
                target_position=messages.Position(x=position.x, y=position.y),
            )
        )

    def choose_origin(self, position: Position[float]):
        self._websocket_client.send(
            messages.ChooseOriginMessage(
                token=self._token,
                origin_position=messages.Position(x=position.x, y=position.y),
            )
        )

    async def _loop(self):
        while True:
            try:
                await asyncio.sleep(self._loop_interval)
                self._websocket_client.send(
                    messages.GetPlayerInfoMessage(
                        token=self._token,
                    )
                )
                self._websocket_client.send(
                    messages.GetMapMessage(
                        token=self._token,
                    )
                )

            except Exception as e:
                logging.error(f"error occurred in agent loop: {e}")

    def _on_message(self, message: messages.Message):
        try:
            msg_dict = message.msg
            msg_type = msg_dict["messageType"]

            if msg_type == "ERROR":
                logging.error(f"error from server: {msg_dict['message']}")

            elif msg_type == "PLAYERS_INFO":
                self._all_player_info = [
                    PlayerInfo(
                        id=data["playerId"],
                        armor=data["armor"],
                        health=data["health"],
                        speed=data["speed"],
                        firearm=data["firearm"]["name"],
                        range=data["firearm"]["distance"],
                        position=Position(
                            x=data["position"]["x"], y=data["position"]["y"]
                        ),
                        inventory=[
                            Item(kind=item["name"], count=item["num"])
                            for item in data["inventory"]
                        ],
                    )
                    for data in msg_dict["players"]
                ]

            elif msg_type == "MAP":
                self._map = Map(
                    length=msg_dict["length"],
                    obstacles=[
                        Position(
                            x=wall["wallPositions"]["x"], y=wall["wallPositions"]["y"]
                        )
                        for wall in msg_dict["walls"]
                    ],
                )

            elif msg_type == "SUPPLIES":
                self._supplies = [
                    Supply(
                        kind=supply["name"],
                        position=Position(
                            x=supply["position"]["x"], y=supply["position"]["y"]
                        ),
                        count=supply["numb"],
                    )
                    for supply in msg_dict["supplies"]
                ]

            elif msg_type == "SAFE_ZONE":
                self._safe_zone = SafeZone(
                    center=Position(
                        x=msg_dict["center"]["x"], y=msg_dict["center"]["y"]
                    ),
                    radius=msg_dict["radius"],
                )

            elif msg_type == "PLAYER_ID":
                self._id = msg_dict["playerId"]

        except Exception as e:
            logging.error(f"error occurred in message handling: {e}")
