from typing import List, Optional

from agent import map, player, supplies, safezone
from agent.agent import Agent
from agent.logger import Logger

class AgentEntry(Agent):
    def __init__(self):
        super().__init__()
        self.Logger = Logger("AgentEntry")

    async def initialize(self):
        await self._initialize()

    async def finalize(self):
        await self._finalize()

    def abandon(self, num: int, targetSupply: str):
        '''
        Abandon the supply.
        '''
        try:
            self._abandon(num, targetSupply)
        except Exception as e:
            self.Logger.error("Failed to abandon: ", e)

    def pick_up(self, targetSupply: str, num: int, x: float, y: float):
        '''
        Pick up the supply.
        '''
        try:
            self._pick_up(targetSupply, num, x, y)
        except Exception as e:
            self.Logger.error("Failed to pick up: ", e)

    def switch_arm(self, targetFirearm: str):
        '''
        Switch the firearm.
        '''
        try:
            self._switch_arm(targetFirearm)
        except Exception as e:
            self.Logger.error("Failed to switch arm: ", e)

    def use_medicine(self, medicineName: str):
        '''
        Use the medicine.
        '''
        try:
            self._use_medicine(medicineName)
        except Exception as e:
            self.Logger.error("Failed to use medicine: ", e)

    def use_grenade(self, x: float, y: float):
        '''
        Use the grenade.
        '''
        try:
            self._use_grenade(x, y)
        except Exception as e:
            self.Logger.error("Failed to use grenade: ", e)

    def move(self, x: float, y: float):
        '''
        Move to the position.
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
        Attack the position.
        '''
        try:
            self._attack(x, y)
        except Exception as e:
            self.Logger.error("Failed to attack: ", e)

    def choose_origin(self, x: float, y: float):
        '''
        Choose the origin.
        '''
        try:
            self._choose_origin(x, y)
        except Exception as e:
            self.Logger.error("Failed to choose origin: ", e)

    def get_player_info(self) -> Optional[List[player.Player]]:
        '''
        Get the player info.
        '''
        return self.PlayerInfo

    def get_map(self) -> Optional[map.Map]:
        '''
        Get the map info.
        '''
        return self.Map

    def get_supplies(self) -> Optional[List[supplies.Supply]]:
        '''
        Get the supplies info.
        '''
        return self.Supplies

    def get_safe_zone(self) -> Optional[safezone.SafeZone]:
        '''
        Get the safe zone info.
        '''
        return self.SafeZone
