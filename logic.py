import logging
from typing import List

from agent.agent import Agent
from agent.position import Position
from agent.path_finding import find_path_befs

path: List[Position[int]] = []


async def setup(agent: Agent):
    # Your code here.
    pass


async def loop(agent: Agent):
    # Your code here.
    # Here is an example of how to use the agent.
    # Always move to the opponent's position, keep one cell away from the
    # opponent, and attack the opponent.

    player_info_list = agent.all_player_info
    assert player_info_list is not None

    self_id = agent.self_id
    assert self_id is not None

    self_info = player_info_list[self_id]
    opponent_info = player_info_list[1 - self_id]

    game_map = agent.map
    assert game_map is not None

    self_position_int = Position[int](
        int(self_info.position.x), int(self_info.position.y)
    )
    opponent_position_int = Position[int](
        int(opponent_info.position.x), int(opponent_info.position.y)
    )

    global path

    if self_position_int not in path or opponent_position_int not in path:
        path = find_path_befs(game_map, self_position_int, opponent_position_int)

        if len(path) == 0:
            logging.info("no path found")
            return

        logging.info(f"path: {path}")

    while path[0] != self_position_int:
        path.pop(0)

    if len(path) > 1:
        next_position_int = path[1]
        next_position = Position[float](
            float(next_position_int.x) + 0.5, float(next_position_int.y) + 0.5
        )

        agent.move(next_position)
        logging.info(f"moving from {self_info.position} to {next_position}")
        return

    agent.attack(opponent_info.position)
