import argparse
import asyncio
import logging

from agent.agent import Agent

# from logic import loop, setup
from logic_example import loop, setup


class Options:
    def __init__(self, server: str, token: str):
        self.server = server
        self.token = token


DEFAULT_SERVER = "ws://localhost:14514"
DEFAULT_TOKEN = "1919810"
DEFAULT_LOOP_INTERVAL = 0.1  # In seconds.


async def main():
    options = parse_options()

    agent = Agent(options.token)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info(f"{agent} is starting with server {options.server}")

    await agent.connect(options.server)

    is_previous_game_ready = False
    is_setup = False

    while True:
        await asyncio.sleep(DEFAULT_LOOP_INTERVAL)

        if not agent.is_game_ready():
            if is_previous_game_ready:
                logging.error(f"{agent} is no longer in a ready game")
                is_previous_game_ready = False

            logging.debug(f"{agent} is waiting for the game to be ready")
            continue
        if not is_previous_game_ready:
            logging.info(f"{agent} is now in a ready game")
            is_previous_game_ready = True

        if not is_setup:
            await setup(agent)
            logging.info(f"{agent} is now set up")
            is_setup = True

        await loop(agent)


def parse_options() -> Options:
    parser = argparse.ArgumentParser("agent")
    parser.add_argument(
        "--server", type=str, help="Server address", default=DEFAULT_SERVER
    )
    parser.add_argument("--token", type=str, help="Agent token", default=DEFAULT_TOKEN)
    args = parser.parse_args()
    return Options(server=args.server, token=args.token)


if __name__ == "__main__":
    asyncio.run(main())
