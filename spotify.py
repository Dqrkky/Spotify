import asyncio
import websockets
import datetime
import json
import shared

class WebsocketRaw:
    def __init__(self, data :dict=None):
        self.data :dict = data
    def todict(self):
        return self.__dict__

class WebsocketPing:
    def __init__(self, time :datetime.datetime=None):
        self.time :datetime.datetime = time
    def todict(self):
        return self.__dict__

class Spotify:
    def __init__(self, access_token: str = None):
        self.event_handlers = {}
        self.config = {
            "spotify": {
                "getaway": {
                    "websocket": "wss://dealer.spotify.com"
                },
                "access_token": access_token if access_token != None and isinstance(access_token, str) else None
            }
        }
        self.shared = shared.Shared()
    def event(self, event_type=None):
        return self._register_event(event_type=event_type)
    def _register_event(self, event_type=None):
        return self.decorator(event_type) if event_type else self.decorator
    def decorator(self, event_type=None):
        if event_type:
            if event_type.__name__ not in self.event_handlers:
                self.event_handlers[event_type.__name__] = event_type
            return event_type
    async def trigger_event(self, event_name, event_data):
        if event_name in self.event_handlers:
            await self.event_handlers[event_name](event_data)
    async def send_ping(self, websocket):
        while True:
            await websocket.ping()
            await self.trigger_event("on_websocket_ping", WebsocketPing(time=datetime.datetime.now()))
            await asyncio.sleep(5)
    async def receive_data(self, websocket):
        while True:
            data = await websocket.recv()
            await self.trigger_event("on_websocket_raw", WebsocketRaw(data=json.loads(data)))
    async def start(self):
        async with websockets.connect(
                f'{self.config["spotify"]["getaway"]["websocket"]}?{self.shared.dtsup(d1ct={
                    "access_token": self.config["spotify"]["access_token"]
                })}'
        ) as websocket:
            ping_task = asyncio.create_task(self.send_ping(websocket))
            data_task = asyncio.create_task(self.receive_data(websocket))
            await asyncio.gather(ping_task, data_task)
    def run(self):
        asyncio.run(self.start())