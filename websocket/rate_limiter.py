from websocket.exceptions import WebSocketTooManyRequests


async def websocket_callback(ws, expire):
    raise WebSocketTooManyRequests("Too many request")