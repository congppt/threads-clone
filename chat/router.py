from json import JSONDecodeError
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from chat import service
from chat.schemas import ChatBase, ChatDisplay, ChatMessages, ChatPage
from db.database import get_cache, get_db_async
from db.models.user import User
from dependencies import get_current_user_async
from redis.asyncio import Redis
from fastapi_limiter.depends import WebSocketRateLimiter
from websocket.exceptions import WebSocketTooManyRequests
from websocket.rate_limiter import websocket_callback
from chat.service import socket_manager


logger = logging.getLogger(__name__)
chat_router = APIRouter(prefix="/chat",  tags=["Chat"])

@chat_router.post("", response_model=ChatDisplay, summary="Create new chat (if not exist for direct type)")
async def try_create_chat_async(request: ChatBase, user: User = Depends(get_current_user_async), db: AsyncSession = Depends(get_db_async)):
    return await service.try_create_chat_async(request, user, db)

@chat_router.get("/{id}/messages", response_model=ChatMessages)
async def get_chat_messages_async(id: Annotated[int, Path(ge=1)], limit: Annotated[int, Query(10, ge=1)], before_message_id: Annotated[int | None, Query(None, ge=1)], user: User = Depends(get_db_async), db: AsyncSession = Depends(get_db_async)):
    messages, has_more = await service.get_chat_messages_async(id, limit, before_message_id, user, db)
    return ChatMessages(messages = messages, has_more = has_more)

@chat_router.get("", response_model=ChatPage)
async def get_user_chats_async(limit: Annotated[int, Query(10, ge=1)], before_id: Annotated[int | None, Query(None, ge=1)], user: User = Depends(get_db_async), db: AsyncSession = Depends(get_db_async)):
    chats, has_more = await service.get_user_chats_async(limit, before_id, user, db)
    return ChatPage(chats = chats, has_more = has_more)

@chat_router.websocket("/ws")
async def chat_websocket_endpoint(ws: WebSocket, user: User = Depends(get_current_user_async), db: AsyncSession = Depends(get_db_async), cache: Redis = Depends(get_cache)):
    chat_ids = await service.start_listening_async(ws, user, db, cache)
    rate_limiter = WebSocketRateLimiter(times=50, seconds=10, callback=websocket_callback)
    try:
        while True:
            try:
                data: dict = await ws.receive_json()
                await rate_limiter(ws)
                if not (message_type:= data.get("type")):
                    await socket_manager.send_error("Message type not defined")
                    continue
                if not (handler := socket_manager.handlers.get(message_type)):
                    await socket_manager.send_error(f"Type {message_type} was not found")
                    continue
                await handler(ws=ws, db=db, cache=cache, data=data, user=user, chat_ids=chat_ids)
            except (JSONDecodeError, AttributeError) as excinfo:
                logger.exception(f"Websocket error, detail: {excinfo}")
                await socket_manager.send_error("Wrong message format", ws)
                continue
            except ValueError as excinfo:
                logger.exception(f"Websocket error, detail: {excinfo}")
                await socket_manager.send_error("Could not validate incoming message", ws)

            except WebSocketTooManyRequests:
                logger.exception(f"User: {user.username} sent too many ws requests")
                await socket_manager.send_error("You have sent too many requests", ws)
    except WebSocketDisconnect:
        logging.info("Websocket is disconnected")
        # unsubscribe user websocket connection from all chats
        if chat_ids:
            for chat_id in chat_ids:
                await socket_manager.remove_user_from_channel_async(chat_id, ws)
            await socket_manager.pubsub_client.disconnect_async()
        await socket_manager.remove_user_websocket_async(user.id, ws)
            


    