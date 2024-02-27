import spotify

sp = spotify.Spotify(
    token=""
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

@sp.event
async def on_user_interaction_raw(ctx :spotify.UserInteraction):
    print(ctx.todict())

try:
    sp.run()
except Exception as e:
    print(f'Error Type : {type(e).__name__} | Error : {e}')