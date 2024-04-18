import argparse

from . import map, player, safezone, supplies
from .connection import message
from .connection.client import Client
from .logger import Logger


class Agent:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", type=str, default="localhost")
        parser.add_argument("--port", type=int, default=14514)
        parser.add_argument("--token", type=str, default="")
        args = parser.parse_args()

        self._client = Client(host=args.host, port=args.port)
        self._client.register_message_handler(self._update)
        self._token = args.token

        self._logger = Logger("Agent")

        self.PlayerInfo = None
        self.Map = None
        self.Supplies = None
        self.SafeZone = None
        self.PlayerId = None

    async def _initialize(self):
        """
        Initialize the agent.
        """
        self._logger.info("Initializing...")
        await self._client.run()
        self._get_player_info()

    async def _finalize(self):
        """
        Finalize the agent.
        """
        self._logger.info("Finalizing...")
        await self._client.stop()

    def _abandon(self, num: int, targetSupply: str):
        """
        Abandon the supply.
        """
        self._send(
            message.PerformAbandonMessage(
                token=self._token, numb=num, targetSupply=targetSupply
            )
        )

    def _pick_up(self, targetSupply: str, num: int, x: float, y: float):
        """
        Pick up the supply.
        """
        self._send(
            message.PerformPickUpMessage(
                token=self._token,
                targetSupply=targetSupply,
                num=num,
                targetPosition=message.Position(x=x, y=y),
            )
        )

    def _switch_arm(self, targetFirearm: str):
        """
        Switch the firearm.
        """
        self._send(
            message.PerformSwitchArmMessage(
                token=self._token, targetFirearm=targetFirearm
            )
        )

    def _use_medicine(self, medicineName: str):
        """
        Use the medicine.
        """
        self._send(
            message.PerformUseMedicineMessage(
                token=self._token, medicineName=medicineName
            )
        )

    def _use_grenade(self, x: float, y: float):
        """
        Use the grenade.
        """
        self._send(
            message.PerformUseGrenadeMessage(
                token=self._token, targetPosition=message.Position(x=x, y=y)
            )
        )

    def _move(self, x: float, y: float):
        """
        Move to the destination.
        """
        self._send(
            message.PerformMoveMessage(
                token=self._token, destination=message.Position(x=x, y=y)
            )
        )

    def _stop(self):
        """
        Stop moving.
        """
        self._send(message.PerformStopMessage(token=self._token))

    def _attack(self, x: float, y: float):
        """
        Attack the target.
        """
        self._send(
            message.PerformAttackMessage(
                token=self._token, targetPosition=message.Position(x=x, y=y)
            )
        )

    def _get_player_info(self):
        """
        Get the player information.
        """
        self._send(message.GetPlayerInfoMessage(token=self._token))

    def _get_map(self):
        """
        Get the map information.
        """
        self._send(message.GetMapMessage(token=self._token))

    def _choose_origin(self, x: float, y: float):
        """
        Choose the origin.
        """
        self._send(
            message.ChooseOriginMessage(
                token=self._token, originPosition=message.Position(x=x, y=y)
            )
        )

    def _update(self, message: message.Message):
        """
        Update the game information.
        """
        try:
            try:
                msg_dict = message.msg
                msg_type = msg_dict["messageType"]
            except Exception as e:
                self._logger.error(f"Failed get message type: {e}")

            if msg_type == "ERROR":
                self._logger.warn(
                    f"Received error message from server: {msg_dict['message']}"
                )

            elif msg_type == "PLAYERS_INFO":
                self.PlayerInfo = [
                    player.Player(
                        playerId=data["playerId"],
                        armor=data["armor"],
                        health=data["health"],
                        speed=data["speed"],
                        firearm=player.Firearm(
                            name=data["firearm"]["name"],
                            distance=data["firearm"]["distance"],
                        ),
                        position=player.Position(
                            x=data["position"]["x"], y=data["position"]["y"]
                        ),
                        inventory=player.Inventory(
                            supplies=[
                                player.Item(name=item["name"], num=item["num"])
                                for item in data["inventory"]
                            ]
                        ),
                    )
                    for data in msg_dict["players"]
                ]

            elif msg_type == "MAP":
                self.Map = map.Map(
                    length=msg_dict["length"],
                    walls=[
                        map.Position(
                            x=wall["wallPositions"]["x"], y=wall["wallPositions"]["y"]
                        )
                        for wall in msg_dict["walls"]
                    ],
                )

            elif msg_type == "SUPPLIES":
                self.Supplies = [
                    supplies.Supply(
                        name=supply["name"],
                        position=supplies.Position(
                            x=supply["position"]["x"], y=supply["position"]["y"]
                        ),
                        numb=supply["numb"],
                    )
                    for supply in msg_dict["supplies"]
                ]

            elif msg_type == "SAFE_ZONE":
                self.SafeZone = safezone.SafeZone(
                    center_x=msg_dict["center"]["x"],
                    center_y=msg_dict["center"]["y"],
                    radius=msg_dict["radius"],
                )

            elif msg_type == "PLAYER_ID":
                self.PlayerId = msg_dict["playerId"]

            else:
                self._logger.warn(f'Unknown message type: "{msg_type}"')

        except Exception as e:
            self._logger.error(
                f'Failed to update information of message "{msg_type}": {e}'
            )

    def _send(self, message: message.Message):
        """
        Send a message to the server.
        """
        self._client.send(message)
