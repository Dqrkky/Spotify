import credentials
import spotify

sp = spotify.Spotify(
    access_token=credentials.TOKEN
)

@sp.event
async def on_websocket_raw(ctx :spotify.WebsocketRaw):
    print(ctx.data)

@sp.event
async def on_websocket_ping(ctx :spotify.WebsocketPing):
    print(ctx.time)

sp.run()