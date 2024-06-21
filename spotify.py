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
    def __init__(self, access_token: str = None):
        self.event_handlers = {}
        self.config = {
            "getaway": {
                "api": "https://gew1-spclient.spotify.com",
                "websocket": "wss://dealer.spotify.com"
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
            },
            "ping_interval": 5,
            "access_token": access_token if access_token and isinstance(access_token, str) else None
        }
        with requests.Session() as rss:
            self.rss = rss
        self.shared = shared.Shared(
            rss=self.rss
        )
        if hasattr(self, "rss") and self.rss and isinstance(self.rss, requests.Session) and \
        hasattr(self, "config") and self.config and isinstance(self.config, dict) and \
        "headers" in self.config and self.config["headers"] and isinstance(self.config["headers"], dict):
            self.rss.headers.update(self.config["headers"])
    def request(self, config :dict=None):
        if config and isinstance(config, dict):
            req = self.rss.request(
                *self.shared.convert_json_to_values(
                    config=config
                )
            )
            if req.status_code == 200:
                return req
    def event(self, event_type=None):
        return self._register_event(event_type=event_type)
    def _register_event(self, event_type=None):
        return self.decorator(event_type) if event_type else self.decorator
    def decorator(self, event_type=None):
        if event_type:
            if event_type.__name__ not in self.event_handlers:
                self.event_handlers[event_type.__name__] = event_type
            return event_type
    async def trigger_event(self, event_name=None, event_data=None):
        if event_name and event_data:
            if event_name in self.event_handlers:
                await self.event_handlers[event_name](event_data)
    async def send_ping(self, websocket=None, ping_interval :int=None):
        if websocket and ping_interval and isinstance(ping_interval, int):
            while True:
                await websocket.ping()
                await self.trigger_event(
                    event_name="on_websocket_ping",
                    event_data=WebsocketPing(
                      time=datetime.datetime.now()
                    )
                )
                await asyncio.sleep(ping_interval)
    async def receive_data(self, websocket=None):
        if websocket:
            while True:
                data = await websocket.recv()
                if data:
                    try:
                        loaded_data = json.loads(
                            data
                        )
                    except Exception as e:
                        loaded_data = None
                        print(f"Error Type : {tye(e).__name__}\nError : {e.__name__}")
                    if loaded_data and isinstance(loaded_data, dict):
                        if "headers" in loaded_data and loaded_data["headers"] and isinstance(loaded_data["headers"], dict):
                            if "Spotify-Connection-Id" in loaded_data["headers"] and loaded_data["headers"]["Spotify-Connection-Id"] and isinstance(loaded_data["headers"]["Spotify-Connection-Id"], str):
                                verified = self.verifydevice(
                                    spotify_connection_id=loaded_data["headers"]["Spotify-Connection-Id"]
                                )
                                if verified:
                                    await self.trigger_event(
                                        event_name="on_connection_verify",
                                        event_data=ConnectionVerify(
                                            data=verified
                                        )
                                    )
                            if "content-type" in loaded_data["headers"] and loaded_data["headers"]["content-type"] and isinstance(loaded_data["headers"]["content-type"], str):
                                if "application/json" == loaded_data["headers"]["content-type"]:
                                    if "payloads" in loaded_data and loaded_data["payloads"] and isinstance(loaded_data["payloads"], list) and len(loaded_data["payloads"]) > 0:
                                        if loaded_data["payloads"][0] and isinstance(loaded_data["payloads"][0], dict):
                                            await self.trigger_event(
                                                event_name="on_websocket_raw",
                                                event_data=WebsocketRaw(
                                                    data=loaded_data["payloads"][0]
                                                )
                                            )
                            if "Content-Type" in loaded_data["headers"] and loaded_data["headers"]["Content-Type"] and isinstance(loaded_data["headers"]["Content-Type"], str):
                                if "text/plain" == loaded_data["headers"]["Content-Type"]:
                                    if "payloads" in loaded_data and loaded_data["payloads"] and isinstance(loaded_data["payloads"], list) and len(loaded_data["payloads"]) > 0:
                                        if loaded_data["payloads"][0] and isinstance(loaded_data["payloads"][0], str):
                                            await self.trigger_event(
                                                event_name="on_user_interaction_raw", 
                                                event_data=UserInteraction(
                                                    data=json.loads(
                                                        loaded_data["payloads"][0]
                                                    )
                                                )
                                            )
    async def start(self):
        if hasattr(self, "config") and self.config and isinstance(self.config, dict) and \
        "ping_interval" in self.config and self.config["ping_interval"] and isinstance(self.config["ping_interval"], int) and \
        "access_token" in self.config and self.config["access_token"] and isinstance(self.config["access_token"], str) and \
        "getaway" in self.config and self.config["getaway"] and isinstance(self.config["getaway"], dict) and \
        "api" in self.config["getaway"] and self.config["getaway"]["api"] and isinstance(self.config["getaway"]["api"], str):
            async with websockets.connect(
                self.shared.construct(
                    url=self.config["getaway"]["websocket"],
                    params={
                        "access_token": self.config["access_token"]
                    }
                )
            ) as websocket:
                ping_task = asyncio.create_task(
                    self.send_ping(
                        websocket=websocket,
                        ping_interval=self.config["ping_interval"]
                    )
                )
                data_task = asyncio.create_task(
                    self.receive_data(
                        websocket=websocket
                    )
                )
                await asyncio.gather(
                    ping_task,
                    data_task
                )
    def generate_hex_string(self, length :int=None):
        if length and isinstance(length, int):
            hex_characters = '0123456789abcdef'
            return ''.join(random.choice(hex_characters) for _ in range(length))
    def hex_to_ascii(self, hex_string :str=None):
        if hex_string and isinstance(hex_string, str):
            ascii_string = ''
            for i in range(0, len(hex_string), 2):
                ascii_string += chr(int(hex_string[i:i+2], 16))
            return ascii_string
    def verifydevice(self, spotify_connection_id :str=None):
        if hasattr(self, "config") and self.config and isinstance(self.config, dict) and \
        "access_token" in self.config and self.config["access_token"] and isinstance(self.config["access_token"], dict) and \
        "getaway" in self.config and self.config["getaway"] and isinstance(self.config["getaway"], dict) and \
        "api" in self.config["getaway"] and self.config["getaway"]["api"] and isinstance(self.config["getaway"]["api"], str):
            if spotify_connection_id and isinstance(spotify_connection_id, str):
                config = {
                    "method": "put",
                    "url": f"{self.config['getaway']['api']}/connect-state/v1/devices/hobs_{self.hex_to_ascii(hex_string=self.generate_hex_string(length=24))}",
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
                        "Authorization": f'Bearer {self.config["access_token"]}',
                        "X-Spotify-Connection-Id": spotify_connection_id
                    }
                }
                req = self.request(
                    config=config
                )
                if req:
                    return req.json()
    def run(self):
        asyncio.run(
            self.start()
        )