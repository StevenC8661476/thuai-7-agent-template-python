# This is an example of the logic file. The logic file is where you write your code to control the agent.

from agent.agent import Agent, Position, PlayerInfo
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.best_first import BestFirst
from pathfinding.finder.a_star import AStarFinder
import random
import logging
import math


def create_logic():
    # Add variables
    have_got_map = False
    map_array = None
    path = None
    path_number = 1
    last_position = None
    stuck_tick = 0

    async def setup(agent: Agent):
        # You can choose an original position when the game is at stage Preparing.
        # If you don't choose an original position or the position is invalid,
        # the game will choose a random position for you.
        # Here we choose (0, 0) and wait for 10 seconds until the game starts.

        # logging.info("Choosing origin (0, 0)")
        # agent.choose_origin(position=Position(0, 0))
        pass

    def reset_path():
        """
        Reset path and path_number to initial values.
        """
        nonlocal path, path_number
        path = None
        path_number = 1

    def get_player_info_by_id(player_id: int, player_info_list: list[PlayerInfo]):
        for player_info in player_info_list:
            if player_info.id == player_id:
                return player_info
        return None

    async def loop(agent: Agent):
        # This is an example of how to find a path to a random destination
        nonlocal have_got_map, map_array, path, path_number, last_position, stuck_tick

        map_length = agent.map.length

        if not have_got_map:
            map_obstacles = agent.map.obstacles
            have_got_map = True
            map_array = np.ones((map_length, map_length))
            for obstacle in map_obstacles:
                map_array[obstacle.x][
                    obstacle.y
                ] = 0  # We can use '0' to represent the wall and '1' to represent the path
                # write the map_array to the log
            logging.info(f"Map: {map_array}")

        # Get current player position
        player_id = agent.self_id
        player_info: PlayerInfo = get_player_info_by_id(
            player_id, agent.all_player_info
        )
        current_x, current_y = player_info.position.x, player_info.position.y

        # Find a path to the destination
        if path is None or len(path) == 0:
            # Randomly choose a destination within distance 20 and not a wall
            destination_x = random.randint(
                max(0, int(current_x) - 20), min(map_length - 1, int(current_x) + 20)
            )
            destination_y = random.randint(
                max(0, int(current_y) - 20), min(map_length - 1, int(current_y) + 20)
            )

            while (
                abs(destination_x - current_x) + abs(destination_y - current_y)
            ) > 20 or map_array[destination_x][destination_y] == 1:
                destination_x = random.randint(
                    max(0, int(current_x) - 20),
                    min(map_length - 1, int(current_x) + 20),
                )
                destination_y = random.randint(
                    max(0, int(current_y) - 20),
                    min(map_length - 1, int(current_y) + 20),
                )

            # Create a grid representation of the map_array
            grid = Grid(matrix=map_array)
            start = grid.node(int(current_x), int(current_y))
            end = grid.node(int(destination_x), int(destination_y))
            logging.info(f"Start: ({start.x} {start.y}) End: ({end.x} {end.y})")

            # Find a path using BestFirst / A* algorithm
            # finder = BestFirst()
            finder = AStarFinder()
            path, _ = finder.find_path(start, end, grid)
            if path is None or len(path) == 0:
                logging.error("No path found")
            else:
                # log the path node
                logging.info(f"Found path: {path}")
        else:
            # If path is found, move along the path
            if path_number < len(path):
                # Move to the next node in the path
                next_x, next_y = path[path_number]
                target_pos = Position(next_x + 0.5, next_y + 0.5)
                agent.move(target_pos)
                # Increment path_number to move to the next node if the distance to current node is less than 1e-2
                if (
                    abs(target_pos.x - current_x) < 2e-2
                    and abs(target_pos.y - current_y) < 2e-2
                ):
                    logging.info(f"Moving to ({next_x}, {next_y})")
                    path_number += 1
            else:
                reset_path()

            if last_position is not None:
                if (
                    math.sqrt(
                        (last_position.x - current_x) ** 2
                        + (last_position.y - current_y) ** 2
                    )
                    < 2e-2
                ):
                    stuck_tick += 1
                else:
                    stuck_tick = 0

            if stuck_tick > 20:
                logging.error("Agent is stuck")
                stuck_tick = 0
                reset_path()

            last_position = Position(current_x, current_y)

    return setup, loop


setup, loop = create_logic()
