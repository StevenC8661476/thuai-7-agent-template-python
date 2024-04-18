"""The logger APIs.

The logger API is the API that can be used to log messages.
"""

import threading
from datetime import datetime
from enum import Enum

from termcolor import cprint

class Logger:
    _FORMAT = ""
    class Level(Enum):
        DEBUG = 0
        INFO = 1
        WARN = 2
        ERROR = 3

    _lock = threading.Lock()

    def __init__(self, namespace: str, level: Level = Level.INFO) -> None:
        super().__init__()

        self._namespace = namespace
        self._level = level

    def set_level(self, level: Level):
        self._level = level

    def debug(self, message: str) -> None:
        if Logger.Level.DEBUG.value < self._level.value:
            return

        with Logger._lock:
            cprint(f'{Logger._get_current_time_string()} ', color='cyan', end='')
            cprint(f'DEBUG ', color='dark_grey', end='')
            cprint(f'[{self._namespace}] {message}', color='dark_grey', end='')
            print()

    def info(self, message: str) -> None:
        if Logger.Level.INFO.value < self._level.value:
            return

        with Logger._lock:
            cprint(f'{Logger._get_current_time_string()} ', color='cyan', end='')
            cprint(f'INFO  ', color='blue', end='')
            cprint(f'[{self._namespace}] {message}', color='white', end='')
            print()

    def warn(self, message: str) -> None:
        if Logger.Level.WARN.value < self._level.value:
            return

        with Logger._lock:
            cprint(f'{Logger._get_current_time_string()} ', color='cyan', end='')
            cprint(f'WARN  ', color='yellow', end='')
            cprint(f'[{self._namespace}] {message}', color='yellow', end='')
            print()

    def error(self, message: str) -> None:
        if Logger.Level.ERROR.value < self._level.value:
            return

        with Logger._lock:
            cprint(f'{Logger._get_current_time_string()} ', color='cyan', end='')
            cprint(f'ERROR ', color='red', end='')
            cprint(f'[{self._namespace}] {message}', color='red', end='')
            print()

    @staticmethod
    def _get_current_time_string() -> str:
        return datetime.now().strftime(f'%H:%M:%S')
