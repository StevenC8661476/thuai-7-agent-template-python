import asyncio
import logging
import queue
import time
from typing import Callable, List

import websockets

from . import messages


class WebsocketClient:
    _MESSAGE_TRANSMISSION_INTERVAL = 0.1
    _MESSAGE_QUEUE_CAPACITY = 5

    def __init__(self, server: str):
        self._connection = None
        self._message_handler_list: List[Callable[[messages.Message], None]] = []
        self._message_queue = queue.Queue(
            maxsize=WebsocketClient._MESSAGE_QUEUE_CAPACITY
        )
        self._task_list: List[asyncio.Task] = []
        self._url = server

    def register_message_handler(
        self, handler: Callable[[messages.Message], None]
    ) -> None:
        self._message_handler_list.append(handler)

    async def run(self) -> None:
        self._connection = await WebsocketClient._try_connect(self._url)
        logging.info(f"Connected to {self._url}")

        self._task_list.append(asyncio.create_task(self._send_loop()))
        self._task_list.append(asyncio.create_task(self._receive_loop()))

    def send(self, message: messages.Message) -> None:
        if self._message_queue.full():
            logging.error("Message queue is full, dropping message")
            return

        self._message_queue.put(message)
        time.sleep(WebsocketClient._MESSAGE_TRANSMISSION_INTERVAL)

    async def stop(self) -> None:
        for task in self._task_list:
            task.cancel()

        await self._connection.close()  # type: ignore

    async def _receive_loop(self) -> None:
        while True:
            try:
                json_string = await self._connection.recv()  # type: ignore
                try:
                    message = messages.Message(str(json_string))
                except Exception as e:
                    logging.error(f"Failed to parse message: {e}")
                    continue

                handler_list = self._message_handler_list.copy()

                for handler in handler_list:
                    handler(message)

            except Exception as e:
                logging.error(f"Failed to receive message: {e}")
                logging.info("Trying to reconnect...")
                self._connection = await WebsocketClient._try_connect(self._url)

    async def _send_loop(self) -> None:
        while True:
            try:
                if not self._message_queue.empty():
                    message: messages.Message = self._message_queue.get()
                    try:
                        json_string = message.json()
                    except Exception as e:
                        logging.error(f"Failed to serialize message: {e}")
                        continue

                    try:
                        await self._connection.send(json_string)  # type: ignore

                    except Exception as e:
                        logging.error(f"Failed to send message: {e}")

                await asyncio.sleep(WebsocketClient._MESSAGE_TRANSMISSION_INTERVAL)

            except Exception as e:
                logging.error(f"Unexpected error occured in send loop: {e}")

    @staticmethod
    async def _try_connect(url: str) -> websockets.WebSocketClientProtocol:  # type: ignore
        logging.info(f"Trying to connect to {url}")

        is_connected = False
        while not is_connected:
            try:
                return await websockets.connect(url)  # type: ignore

            except Exception as e:
                logging.error(f"Failed to connect to {url}: {e}")
                logging.info("Retrying...")
