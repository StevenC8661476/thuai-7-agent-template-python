from typing import List, Optional

from agent import map, player, supplies, safezone
from agent.agent import Agent
from agent.logger import Logger

class AgentEntry(Agent):
    def __init__(self):
        super().__init__()
        self.Logger = Logger("AgentEntry")

    async def initialize(self):
        '''
        This is not for you.
        '''
        await self._initialize()

    async def finalize(self):
        '''
        This is not for you.
        '''
        await self._finalize()

    def abandon(self, num: int, targetSupply: str):
        '''
        Abandon the supply.
        num: The number of supplies to abandon.
        targetSupply: The name of the supply to abandon.
        '''
        try:
            self._abandon(num, targetSupply)
        except Exception as e:
            self.Logger.error("Failed to abandon: ", e)

    def pick_up(self, targetSupply: str, num: int, x: float, y: float):
        '''
        Pick up the supply.
        num: The number of supplies to pick up.
        targetSupply: The name of the supply to pick up.
        x: The x-coordinate of the supply.
        y: The y-coordinate of the supply.
        '''
        try:
            self._pick_up(targetSupply, num, x, y)
        except Exception as e:
            self.Logger.error("Failed to pick up: ", e)

    def switch_arm(self, targetFirearm: str):
        '''
        Switch the firearm.
        targetFirearm: The name of the firearm to switch to.
        '''
        try:
            self._switch_arm(targetFirearm)
        except Exception as e:
            self.Logger.error("Failed to switch arm: ", e)

    def use_medicine(self, medicineName: str):
        '''
        Use the medicine.
        medicineName: The name of the medicine to use.
        '''
        try:
            self._use_medicine(medicineName)
        except Exception as e:
            self.Logger.error("Failed to use medicine: ", e)

    def use_grenade(self, x: float, y: float):
        '''
        Use the grenade.
        x: The x-coordinate of the target position.
        y: The y-coordinate of the target position.
        '''
        try:
            self._use_grenade(x, y)
        except Exception as e:
            self.Logger.error("Failed to use grenade: ", e)

    def move(self, x: float, y: float):
        '''
        Set a position as destination and move towards it.
        x: The x-coordinate of the destination.
        y: The y-coordinate of the destination.
        '''
        try:
            self._move(x, y)
        except Exception as e:
            self.Logger.error("Failed to move: ", e)

    def stop(self):
        '''
        Stop moving.
        '''
        try:
            self._stop()
        except Exception as e:
            self.Logger.error("Failed to stop: ", e)

    def attack(self, x: float, y: float):
        '''
        Aim at a position and attack.
        x: The x-coordinate of the target position.
        y: The y-coordinate of the target position.
        '''
        try:
            self._attack(x, y)
        except Exception as e:
            self.Logger.error("Failed to attack: ", e)

    def choose_origin(self, x: float, y: float):
        '''
        Choose the origin. Can only be called when the game is at stage Preparing.
        x: The x-coordinate of the origin.
        y: The y-coordinate of the origin.
        '''
        try:
            self._choose_origin(x, y)
        except Exception as e:
            self.Logger.error("Failed to choose origin: ", e)

    def get_player_info(self) -> Optional[List[player.Player]]:
        '''
        Get the player info. Returns null if the game is not ready.
        '''
        return self.PlayerInfo

    def get_map(self) -> Optional[map.Map]:
        '''
        Get the map info. Returns null if the game is not ready.
        '''
        return self.Map

    def get_supplies(self) -> Optional[List[supplies.Supply]]:
        '''
        Get the supplies info. Returns null if the game is not ready.
        '''
        return self.Supplies

    def get_safe_zone(self) -> Optional[safezone.SafeZone]:
        '''
        Get the safe zone info. Returns null if the game is not ready.
        '''
        return self.SafeZone
