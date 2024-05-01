import argparse
import asyncio
import logging

from agent.agent import Agent
from logic import loop, setup


class Options:
    def __init__(self, logging_level: int, server: str, token: str):
        self.logging_level = logging_level
        self.server = server
        self.token = token


DEFAULT_SERVER = "ws://localhost:14514"
DEFAULT_TOKEN = "1919810"
DEFAULT_LOOP_INTERVAL = 0.1  # In seconds.
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"


async def main():
    options = parse_options()

    logging.basicConfig(level=options.logging_level, format=LOGGING_FORMAT)

    agent = Agent(options.token, DEFAULT_LOOP_INTERVAL)
    logging.info(f"{agent} is starting with server {options.server}")

    await agent.connect(options.server)

    is_previous_connected = False
    is_previous_game_ready = False
    is_setup = False

    while True:
        await asyncio.sleep(DEFAULT_LOOP_INTERVAL)

        if not agent.is_connected():
            if is_previous_connected:
                logging.error(f"{agent} is no longer connected")
                is_previous_connected = False

            logging.debug(f"{agent} is waiting for the connection")
            continue

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
        "--logging-level",
        type=int,
        help="Logging level",
        default=logging.INFO,
        choices=[
            logging.CRITICAL,
            logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
        ],
    )
    parser.add_argument(
        "--server", type=str, help="Server address", default=DEFAULT_SERVER
    )
    parser.add_argument("--token", type=str, help="Agent token", default=DEFAULT_TOKEN)
    args = parser.parse_args()
    return Options(
        logging_level=args.logging_level, server=args.server, token=args.token
    )


if __name__ == "__main__":
    asyncio.run(main())
