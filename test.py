import credentials
import spotify

sp = spotify.Spotify(
    token=credentials.TOKEN
)

@sp.event
async def on_connection_verify(ctx :spotify.ConnectionVerify):
    print(ctx.todict())

@sp.event
async def on_websocket_raw(ctx :spotify.WebsocketRaw):
    print(ctx.todict())

@sp.event
async def on_websocket_ping(ctx :spotify.WebsocketPing):
    print(ctx.todict())

sp.run()