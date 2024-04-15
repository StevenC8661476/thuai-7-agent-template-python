from agent import map, player, supplies
from agent.logger import Logger

from agent_entry import AgentEntry

import asyncio
import traceback

'''
Here are some constants you may need in your agent.
'''
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

'''
In a solution, you will create your own agent to play the game.
NOTE: If you want to do something like waiting for a few seconds,
you should use "await asyncio.sleep()" rather than "time.sleep()".
'''
async def solution(agent: AgentEntry):
    # You can log some messages to debug your agent with agent.Logger.
    agent.Logger.set_level(Logger.Level.INFO)

    # If you find that you are dropping too many messages,
    # You can try increasing SLEEP_TIME.
    SLEEP_TIME = 0.02

    # Wait until the game is ready.
    while agent.get_map() is None or agent.get_player_info() is None\
        or agent.get_supplies() is None or agent.get_safe_zone() is None\
        or agent.get_player_id() is None:
        await asyncio.sleep(SLEEP_TIME)

    agent.Logger.info(f"PlayerId of the agent: {agent.get_player_id()}")

    # You can choose an original position when the game is at stage Preparing.
    # If you don't choose an original position or the position is invalid,
    # the game will choose a random position for you.
    # Here we choose (0, 0) and wait for 10 seconds until the game starts.
    agent.Logger.info("Choosing origin (0, 0)")
    agent.choose_origin(0, 0)
    await asyncio.sleep(10)

    while True:
        # Your solution here.
        # Note that anytime you want to end, "continue", or "break" a loop,
        # You should add "await asyncio.sleep(SLEEP_TIME)" before them.
        x = random.random() * agent.get_map().Length
        y = random.random() * agent.get_map().Length
        agent.Logger.info(f"Moving to ({x}, {y})")
        agent.move(x, y)

        await asyncio.sleep(SLEEP_TIME)   # Do NOT delete this line or your agent may not be able to run.

    # Usually you don't need to add anything after the loop
    return

# Things you can change ends here.
###############################################################################

async def main():
    version = "0.1.0"

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
