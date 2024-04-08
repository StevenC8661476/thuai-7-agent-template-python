import asyncio
import traceback

from agent import map, player, supplies
from agent.logger import Logger

from agent_entry import AgentEntry

async def solution(agent: AgentEntry):

    # You might want to add some initialization here

    agent.Logger.set_level(Logger.Level.DEBUG)

    while agent.get_map() is None or agent.get_player_info() is None or agent.get_supplies() is None:
        continue

    # You need to choose an original position to start the game.
    # We recommend you to choose the origin according to map and supply information.
    agent.choose_origin(0, 0)

    while True:
        # Your solution here
        agent.Logger.info("Attacking (0, 0)")
        agent.attack(0, 0)

        # If you find that you are dropping too many messages, sleep more.
        # Or try to optimize your code to perform less actions in one loop.
        await asyncio.sleep(0.02)   # Do NOT delete this line or your agent may not be able to run.

    # Usually you don't need to add anything here
    return

async def main():
    try:
        my_agent = AgentEntry()
        await my_agent.initialize()
        await solution(my_agent)

    except BaseException as e:
        my_agent.Logger.error(f"An unhandled exception is caught while agent is running: {e}")
        my_agent.Logger.error(traceback.format_exc())

    finally:
        await my_agent.finalize()

if __name__ == "__main__":
    asyncio.run(main())
