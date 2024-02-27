import random
import asyncio
import websockets
import datetime
import json
import requests
import shared

class WebsocketRaw:
    def __init__(self, data :dict=None):
        self.data :dict = data
    def todict(self):
        return self.__dict__

class ConnectionVerify:
    def __init__(self, data :dict=None):
        self.data :dict = data
    def todict(self):
        return self.__dict__

class UserInteraction:
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
    def __init__(self, token: str = None):
        self.event_handlers = {}
        self.config = {
            "spotify": {
                "getaway": {
                    "websocket": "wss://dealer.spotify.com"
                },
                "token": token if token != None and isinstance(token, str) else None
            }
        }
        with requests.Session() as rss:
            self.rss = rss
        self.shared = shared.Shared(
            rss=self.rss
        )
    def request(self, config :dict=None):
        if config != None and isinstance(config, dict):
            req = self.rss.request(
                *self.shared.convert_json_to_values(
                    config=config
                )
            )
            if req.status_code == 200:
                return req
    def construct(self, url :str=None, params :dict=None):
        if url != None and isinstance(url, str) and params != None and isinstance(params, dict):
            return f'{url}?{self.shared.dtsup(params)}'
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
            loaded_data = json.loads(data)
            if loaded_data != None and isinstance(loaded_data, dict):
                if "headers" in loaded_data and loaded_data["headers"] != None and isinstance(loaded_data["headers"], dict):
                    if "Spotify-Connection-Id" in loaded_data["headers"] and loaded_data["headers"]["Spotify-Connection-Id"] != None and isinstance(loaded_data["headers"]["Spotify-Connection-Id"], str):
                        verified = self.verifydevice(
                            spotify_connection_id=loaded_data["headers"]["Spotify-Connection-Id"]
                        )
                        if verified != None:
                            await self.trigger_event("on_connection_verify", ConnectionVerify(data=verified))
                    if "content-type" in loaded_data["headers"] and loaded_data["headers"]["content-type"] != None and isinstance(loaded_data["headers"]["content-type"], str):
                        if "application/json" == loaded_data["headers"]["content-type"]:
                            if "payloads" in loaded_data and loaded_data["payloads"] != None and isinstance(loaded_data["payloads"], list) and len(loaded_data["payloads"]) > 0:
                                if loaded_data["payloads"][0] != None and isinstance(loaded_data["payloads"][0], dict):
                                    await self.trigger_event("on_websocket_raw", WebsocketRaw(data=loaded_data["payloads"][0]))
                    if "Content-Type" in loaded_data["headers"] and loaded_data["headers"]["Content-Type"] != None and isinstance(loaded_data["headers"]["Content-Type"], str):
                        if "text/plain" == loaded_data["headers"]["Content-Type"]:
                            if "payloads" in loaded_data and loaded_data["payloads"] != None and isinstance(loaded_data["payloads"], list) and len(loaded_data["payloads"]) > 0:
                                if loaded_data["payloads"][0] != None and isinstance(loaded_data["payloads"][0], str):
                                    await self.trigger_event("on_user_interaction_raw", UserInteraction(data=json.loads(loaded_data["payloads"][0])))
    async def start(self):
        if self.config["spotify"]["token"] != None:
            async with websockets.connect(
                self.construct(
                    url=self.config["spotify"]["getaway"]["websocket"],
                    params={
                        "access_token": self.config["spotify"]["token"]
                    }
                )
            ) as websocket:
                ping_task = asyncio.create_task(self.send_ping(websocket))
                data_task = asyncio.create_task(self.receive_data(websocket))
                await asyncio.gather(ping_task, data_task)
    def generate_hex_string(self, length :int=None):
        if length != None and isinstance(length, int):
            hex_characters = '0123456789abcdef'
            hex_string = ''.join(random.choice(hex_characters) for _ in range(length))
            return hex_string
    def hex_to_ascii(self, hex_string :str=None):
        if hex_string != None and isinstance(hex_string, str):
            ascii_string = ''
            for i in range(0, len(hex_string), 2):
                ascii_string += chr(int(hex_string[i:i+2], 16))
            return ascii_string
    def verifydevice(self, spotify_connection_id :str=None):
        if self.config["spotify"]["token"] != None and spotify_connection_id != None and isinstance(spotify_connection_id, str):
            config = {
                "method": "put",
                "url": f"https://gew1-spclient.spotify.com/connect-state/v1/devices/hobs_{self.hex_to_ascii(self.generate_hex_string(24))}",
                "data": json.dumps({
                    "member_type": "CONNECT_STATE",
                    "device": {
                        "device_info": {
                            "capabilities": {
                                "can_be_player": False,
                                "hidden": True,
                                "needs_full_player_state": True
                            }
                        }
                    }
                }),
                "headers": {
                    "Authorization": f'Bearer {self.config["spotify"]["token"]}',
                    "X-Spotify-Connection-Id": spotify_connection_id
                }
            }
            req = self.request(
                config=config
            )
            if req != None:
                return req.json()
    def run(self):
        asyncio.run(self.start())