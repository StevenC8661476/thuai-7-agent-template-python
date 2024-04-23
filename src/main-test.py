from agent import map, player, supplies
from agent.logger import Logger

from agent_entry import AgentEntry

import asyncio
import traceback

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np

"""
Here are some constants you may need in your agent.
"""
# Names of armors
PRIMARY_ARMOR = "PRIMARY_ARMOR"
PREMIUM_ARMOR = "PREMIUM_ARMOR"

# Names of weapons
SHOTGUN = "S686"
ASSAULT_RIFLE = "M16"
SNIPER_RIFLE = "AWM"
SUBMACHINE_GUN = "VECTOR"

# Names of medicines
BANDAGE = "BANDAGE"
FIRST_AID_KIT = "FIRST_AID"

# Name of bullet
BULLET = "BULLET"

# Name of grenade
GRENADE = "GRENADE"

###############################################################################
# Things you can change starts here.

# You can import something else if you need them.
import random

"""
In a solution, you will create your own agent to play the game.
NOTE: If you want to do something like waiting for a few seconds,
you should use "await asyncio.sleep()" rather than "time.sleep()".
"""


async def get_player_info_by_id(player_id, player_info_list):
    for player_info in player_info_list:
        if player_info.PlayerId == player_id:
            return player_info
    return None


async def solution(agent: AgentEntry):
    # You can log some messages to debug your agent with agent.Logger.
    agent.Logger.set_level(Logger.Level.INFO)

    # If you find that you are dropping too many messages,
    # You can try increasing SLEEP_TIME.
    SLEEP_TIME = 0.02

    # Wait until the game is ready.
    while (
        agent.get_map() is None
        or agent.get_player_info() is None
        or agent.get_supplies() is None
        or agent.get_safe_zone() is None
        or agent.get_player_id() is None
    ):
        await asyncio.sleep(SLEEP_TIME)

    agent.Logger.info(f"PlayerId of the agent: {agent.get_player_id()}")


    agent.Logger.info("Choosing origin (122, 117)")
    agent.choose_origin(117, 112)
    await asyncio.sleep(10)

    have_get_map = False
    map = None
    path = None
    path_number = 1
    while True:
        map_length = agent.get_map().Length

        if not have_get_map:
            map_walls = agent.get_map().Walls
            have_get_map = True
            map = np.zeros((map_length, map_length))
            for wall in map_walls:
                map[wall.X][wall.Y] = 1  # 1 represents wall

        # Get current player position
        player_id = agent.get_player_id()
        player_info: player = await get_player_info_by_id(
            player_id, agent.get_player_info()
        )
        if player_info is None:
            agent.Logger.error(f"Player info not found for playerId: {player_id}")
            await asyncio.sleep(SLEEP_TIME)
            continue
        current_x, current_y = player_info.Position.X, player_info.Position.Y
        # Randomly choose a destination within distance 20 and not a wall
        destination_x = random.randint(
            max(0, int(current_x) - 20), min(map_length - 1, int(current_x) + 20)
        )
        destination_y = random.randint(
            max(0, int(current_y) - 20), min(map_length - 1, int(current_y) + 20)
        )

        while (
            abs(destination_x - current_x) + abs(destination_y - current_y)
        ) > 20 or map[destination_x][destination_y] == 1:
            destination_x = random.randint(
                max(0, int(current_x) - 20), min(map_length - 1, int(current_x) + 20)
            )
            destination_y = random.randint(
                max(0, int(current_y) - 20), min(map_length - 1, int(current_y) + 20)
            )

        if path is None or len(path) == 0:
            # Create a grid representation of the map
            grid = Grid(matrix=map)
            start = grid.node(int(current_x), int(current_y))
            end = grid.node(int(destination_x), int(destination_y))
            print("Start: ", start.x, start.y, "End: ", end.x, end.y)

            # Find a path using A* algorithm
            finder = AStarFinder()
            path, _ = finder.find_path(start, end, grid)
            if path is None or len(path) == 0:
                agent.Logger.error("No path found")
                # print(map.sum())
            else:
                print("Found path: ", path)
        # If path is found, move along the path
        else:
            if path_number < len(path):
                # Move to the next node in the path
                next_x, next_y = path[path_number]
                agent.move(next_x, next_y)
                # Increment path_number to move to the next node if the distance to current node is less than 1e-2
                if abs(next_x - current_x) < 1e-1 and abs(next_y - current_y) < 1e-1:
                    agent.Logger.info(f"Moving to ({next_x}, {next_y})")
                    path_number += 1
            else:
                path_number = 1
                path = None

        await asyncio.sleep(
            SLEEP_TIME
        )  # Do NOT delete this line or your agent may not be able to run.

    # Usually you don't need to add anything after the loop
    return


# Things you can change ends here.
###############################################################################


async def main():
    version = "0.1.1"

    logger = Logger("Main")
    logger.info(f"THUAI7 Agent Template (Python) v{version}")
    logger.info("Copyright (C) 2024 THUASTA")

    try:
        my_agent = AgentEntry()
        await my_agent.initialize()
        await solution(my_agent)

    except Exception as e:
        logger.error(f"An unhandled exception is caught while agent is running: {e}")
        logger.error(traceback.format_exc())

    finally:
        await my_agent.finalize()


if __name__ == "__main__":
    asyncio.run(main())
