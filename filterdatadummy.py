import json

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
            "duration": data["cluster"]["player_state"]["duration"],
            "durationInMinutes": ((int(data["cluster"]["player_state"]["duration"]) / 1000) / 60),
            "devices": [{
                "name": data["cluster"]["devices"][device]["name"],
                "volume": data["cluster"]["devices"][device]["volume"],
                "brand": data["cluster"]["devices"][device]["brand"],
                "model": data["cluster"]["devices"][device]["model"],
                "public_ip": data["cluster"]["devices"][device]["public_ip"],
            } for device in data["devices_that_changed"]]
        }
        print(
            "-" * 50 + "\n" +
            json.dumps(
                obj=c,
                indent=4
            )
            + "\n" + "-" * 50 + "\n"
        )