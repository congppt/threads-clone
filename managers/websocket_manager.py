import asyncio
import json
import logging
from redis.asyncio.client import PubSub
from fastapi import WebSocket
from managers.pubsub_manager import RedisPubSubManager

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.handlers: dict = {}
        self.channel_id_websockets: dict[int, set[WebSocket]] = {}
        self.pubsub_client = RedisPubSubManager()
        self.user_id_websockets: dict[int, set[WebSocket]] = {}
    
    def handler(self, message_type):
        def decorator(func):
            self.handlers[message_type] = func
            return func
        return decorator
    
    async def connect_socket_async(self, ws: WebSocket):
        await ws.accept()
    
    async def add_socket_connection_async(self, user_id: int, ws: WebSocket):
        connections: set = self.user_id_websockets.setdefault(user_id, set())
        connections.add(ws)

    async def add_user_to_channel_async(self, channel_id: int, ws: WebSocket):
        if channel_id in self.channel_id_websockets:
            self.channel_id_websockets[channel_id].add(ws)
        else:
            self.channel_id_websockets[channel_id] = { ws }
            await self.pubsub_client.connect()
            subscriber = await self.pubsub_client.subscribe_async(channel_id)
            asyncio.create_task(self.__pubsub_read_async(subscriber))
    
    async def __pubsub_read_async(self, subscriber: PubSub):
        try:
            while True:
                message = await subscriber.get_message(ignore_subscribe_messages=True)
                if message is None:
                    return                
                chat_id = bytes(message["channel"]).decode("utf-8")
                sockets = self.channel_id_websockets.get(chat_id)
                if not sockets:
                    return
                for socket in sockets:
                    data = bytes(message["data"]).decode("utf-8")
                    await socket.send_text(data)
        except Exception as exc:
            logger.exception(f"Exception occurred: {exc}")

    async def broadcast_to_channel_async(self, channel_id: int, message: str | dict) -> None:
        if isinstance(message, dict):
            message = json.dumps(message)
        await self.pubsub_client.publish_async(channel_id, message)
    async def remove_user_from_channel_async(self, channel_id:int, ws: WebSocket):
        if channel_id not in self.channel_id_websockets:
            return
        self.channel_id_websockets[channel_id].remove(ws)
        if len(self.channel_id_websockets[channel_id]) == 0:
            del self.channel_id_websockets[channel_id]
            logger.info(f"Removing channel {channel_id} from PubSub")
            await self.pubsub_client.unsubscribe_async(channel_id)

    async def remove_user_websocket_async(self, user_id: int, ws: WebSocket):
        if user_id not in self.user_id_websockets:
            return
        self.user_id_websockets[user_id].remove(ws)

    async def send_error(self, message: str, websocket: WebSocket):
        await websocket.send_json({"status": "error", "message": message})
