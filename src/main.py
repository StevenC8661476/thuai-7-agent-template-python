import asyncio
import random
import traceback

from agent import map, player, supplies
from agent.logger import Logger

from agent_entry import AgentEntry

async def solution(agent: AgentEntry):

    # You might want to add some initialization here
    count = 100

    agent.Logger.set_level(Logger.Level.DEBUG)

    while True:

        # Your solution here
        count += 1

        if (count == 150):
            agent.Logger.info("Oh, let's see the map.")
            if agent.get_map() is not None:
                agent.Logger.info(
                    f"Map:\n\
                    {[(wall.X, wall.Y) for wall in agent.get_map().Walls]}"
                )
            else:
                agent.Logger.info("Oh no, it is null.")

        if (200 <= count and count < 500):
            if (count == 200):
                agent.Logger.info("I'm going to run!")
                agent.Logger.set_level(Logger.Level.INFO)
            agent.move(random.uniform(0, 256), random.uniform(0, 256))

        if (count == 1000):
            agent.Logger.warn("I'm tired of running! I'm going to stop!")
            agent.stop()

        if (count == 1500):
            agent.Logger.error("I get bored. Goodbye!")
            break

        '''
        If you find that you are dropping too many messages, sleep more.
        Or try to optimize your code to perform less actions in one loop.
        '''
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
