import websockets

class Client:
    def __init__(self):
        self._ws = None

    def connect(self, uri):
        self._ws = websockets.connect(uri)

    async def send(self, message):
        await self._ws.send(message)

    async def receive(self):
        return await self._ws.recv()
