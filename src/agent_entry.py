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
        self._abandon(num, targetSupply)

    def pick_up(self, targetSupply: str, num: int, x: float, y: float):
        '''
        Pick up the supply.
        '''
        self._pick_up(targetSupply, num, x, y)

    def switch_arm(self, targetFirearm: str):
        '''
        Switch the firearm.
        '''
        self._switch_arm(targetFirearm)

    def use_medicine(self, medicineName: str):
        '''
        Use the medicine.
        '''
        self._use_medicine(medicineName)

    def use_grenade(self, x: float, y: float):
        '''
        Use the grenade.
        '''
        self._use_grenade(x, y)

    def move(self, x: float, y: float):
        '''
        Move to the position.
        '''
        self._move(x, y)

    def stop(self):
        '''
        Stop moving.
        '''
        self._stop()

    def attack(self, x: float, y: float):
        '''
        Attack the position.
        '''
        self._attack(x, y)

    def choose_origin(self, x: float, y: float):
        '''
        Choose the origin.
        '''
        self._choose_origin(x, y)

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
