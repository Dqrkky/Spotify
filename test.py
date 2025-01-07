import spotify
import dotenv
import os
from filterdatadummy import print_json

dotenv.load_dotenv()

sp = spotify.Spotify(
    access_token=os.getenv("TOKEN")
)

@sp.event
async def on_connection_verify(ctx :spotify.ConnectionVerify):
    print_json(ctx.todict())

@sp.event
async def on_websocket_raw(ctx :spotify.WebsocketRaw):
    print_json(ctx.todict())

@sp.event
async def on_websocket_ping(ctx :spotify.WebsocketPing):
    print_json(ctx.todict())

@sp.event
async def on_user_interaction_raw(ctx :spotify.UserInteraction):
    print_json(ctx.todict())

try:
    sp.run()
except Exception as e:
    error = {
        "type": "error",
        "error": list(e.args),
        "error_type": type(e).__name__,
        "error_module": type(e).__module__
    }
    print_json(error)