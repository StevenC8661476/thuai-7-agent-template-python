import asyncio
import random

from agent import map, player, supplies
from agent.logger import Logger

from agent_entry import AgentEntry

async def solution(agent: AgentEntry):

    # You might want to add some initialization here
    count = 100

    agent.Logger.set_level(Logger.Level.DEBUG)

    while True:

        # Your solution here
        agent.Logger.debug(f"There are {count} apples.")
        count += 1

        if (1000 <= count and count < 3000):
            if (count == 1000):
                agent.Logger.info("Too many apples! I'm going to run!")
                agent.Logger.set_level(Logger.Level.INFO)
            agent.move(random.uniform(0, 256), random.uniform(0, 256))

        if (count == 3000):
            agent.Logger.warn("I'm tired of running! I'm going to stop!")
            agent.stop()

        if (count == 4000):
            agent.Logger.info("Oh, let's see who's around me.")
            if agent.get_player_info() is not None:
                agent.Logger.info(
                    f"Players:\n\
                    {[player.PlayerId for player in agent.get_player_info()]}"
                )
            else:
                agent.Logger.info("No one around me.")

        if (count == 5000):
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

    finally:
        await my_agent.finalize()

if __name__ == "__main__":
    asyncio.run(main())
