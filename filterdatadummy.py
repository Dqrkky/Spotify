import json
import os
import requests
import re

def print_json(config :dict=None):
    if config != None and isinstance(config, dict):  # noqa: E711
        if config["type"] == "error":
            print(config)
        if config["type"] != "WebsocketRaw":
            return
        data = config["data"]
        c = {
            "update_reason": data["update_reason"],
            "track": f'https://open.spotify.com/track/{data["cluster"]["player_state"]["track"]["uri"].split(":")[-1]}',
            "devices_that_changed": data["devices_that_changed"],
            "active_device_id": data["cluster"]["active_device_id"],
            "devices": [{
                "id": device["device_id"],
                "device_type": device["device_type"],
                "name": device["name"],
                "volume": device["volume"],
                "brand": device["brand"],
                "model": device["model"],
                "public_ip": ".".join(device["public_ip"].split(".")[:2]+["*"]*2)
            } for device_id, device in data["cluster"]["devices"].items()],
            "message": [json.loads(match[1]) for match in re.findall(r'<script[^>]*type="application/(ld\+json|json)"[^>]*>({.*?})</script>', requests.get(f'https://open.spotify.com/track/{data["cluster"]["player_state"]["track"]["uri"].split(":")[-1]}').text, re.DOTALL)][0]["description"]
        }
        os.system("cls")
        print(
            "-" * 50 + "\n" +
            json.dumps(
                obj=c,
                indent=4
            )
            + "\n" + "-" * 50 + "\n"
        )