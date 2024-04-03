import asyncio
import json
import queue
from typing import Callable, List

import websockets

from ..logger import Logger
from message import *

class Client:
    Message_TRANSMISSION_INTERVAL = 0.01
    Message_QUEUE_CAPACITY = 100

    def __init__(self, host: str, port: int):
        self._connection = None
        self.Logger = Logger("SDK.Client")
        self.Message_handler_list: List[Callable[[Message], None]] = []
        self.Message_queue = queue.Queue(
            maxsize=Client.Message_QUEUE_CAPACITY)
        self._task_list: List[asyncio.Task] = []
        self._url = f"ws://{host}:{port}"

    def registerMessage_handler(self, handler: Callable[[Message], None]) -> None:
        self.Message_handler_list.append(handler)

    async def run(self) -> None:
        self._connection = await Client._try_connect(self._url)
        self.Logger.info(f"Connected to {self._url}")

        self._task_list.append(asyncio.create_task(self._send_loop()))
        self._task_list.append(asyncio.create_task(self._receive_loop()))

    def send(self, message: Message) -> None:
        if self.Message_queue.full():
            self.Logger.error("Message queue is full, dropping message")
            return

        self.Message_queue.put(message)

    async def stop(self) -> None:
        for task in self._task_list:
            task.cancel()

        await self._connection.close() # type: ignore

    async def _receive_loop(self) -> None:
        while True:
            try:
                json_string = await self._connection.recv()  # type: ignore
                message = Message(json_string)

                handler_list = self.Message_handler_list.copy()

                for handler in handler_list:
                    handler(message)

            except Exception as e:
                self.Logger.error(f"Failed to receive message: {e}")
                self.Logger.info("Trying to reconnect...")
                self._connection = await Client._try_connect(self._url)

    async def _send_loop(self) -> None:
        while True:
            try:
                if not self.Message_queue.empty():
                    message: Message = self.Message_queue.get()
                    json_string = message.json()

                    try:
                        await self._connection.send(json_string) # type: ignore

                    except Exception as e:
                        self.Logger.error(f"Failed to send message: {e}")

                await asyncio.sleep(Client.Message_TRANSMISSION_INTERVAL)

            except Exception as e:
                self.Logger.error(f"Unexpected error occured in send loop: {e}")

    @staticmethod
    async def _try_connect(url: str) -> websockets.WebSocketClientProtocol:  # type: ignore
        logger = Logger("SDK.Client")
        logger.info(f"Trying to connect to {url}")

        is_connected = False
        while not is_connected:
            try:
                return await websockets.connect(url)  # type: ignore
            except:
                logger.error(f"Failed to connect to {url}")
                logger.info("Retrying...")
