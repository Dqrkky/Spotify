import spotify

sp = spotify.Spotify(
    access_token=""
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
    error = {
        "error": list(e.args),
        "error_type": type(e).__name__,
        "error_module": type(e).__module__
    }
    print(error)