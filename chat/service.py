import logging
from fastapi import HTTPException, WebSocket, status
from sqlalchemy import and_, desc, select
from sqlalchemy.orm import selectinload
from chat.schemas import ChatBase, ReceiveMessage, SendMessage
from db.models.chat import Chat, ChatType
from db.models.message import Message
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from managers.websocket_manager import WebSocketManager


logger = logging.getLogger(__name__)
socket_manager = WebSocketManager()


async def try_create_chat_async(
    request: ChatBase, user: User, db: AsyncSession
) -> Chat:
    chat = None
    if len(request.user_ids) == 1:
        user_id = next(iter(request.user_ids))
        recipient = await __get_user_by_id_async(user_id, db)
        if recipient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not exist",
            )
        if recipient.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot create chat with self",
            )
        chat = await try_get_direct_chat_async(user, recipient, db)
        if chat is not None:
            return chat
        chat = Chat(type=ChatType.DIRECT)
        if not request.name:
            chat.name = f"Direct {recipient.username}"
        else:
            chat.name = request.name
        chat.users.append(user)
        chat.users.append(recipient)
    else:
        # not implemented
        pass
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


async def __get_user_by_id_async(user_id: int, db: AsyncSession) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user


async def try_get_direct_chat_async(
    user: User, recipient: User, db: AsyncSession
) -> Chat | None:
    query = select(Chat).where(
        Chat.type == ChatType.DIRECT,
        and_(
            Chat.users.any(User.id == user.id), Chat.users.any(User.id == recipient.id)
        ),
    )
    result = await db.execute(query)
    chat = result.scalar_one_or_none()
    return chat


async def get_chat_messages_async(
    id: int, limit: int, before_message_id: int | None, user: User, db: AsyncSession
) -> tuple[list[Message], bool]:
    chat = await get_chat_by_id_async(id, user, db)
    query = select(Message).where(Message.chat == chat).limit(limit + 1)
    if before_message_id is not None:
        query = query.where(Message.id < before_message_id)
    result = await db.execute(query)
    messages = result.scalars().all()
    has_more = len(messages) > limit
    messages = messages[:limit]
    return messages, has_more


async def get_chat_by_id_async(id: int, user: User, db: AsyncSession) -> Chat:
    query = select(Chat).where(Chat.id == id).options(selectinload(Chat.users))
    result = await db.execute(query)
    chat = result.scalar_one_or_none()
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {id} does not exist",
        )
    if user not in chat.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Chat is not accessible"
        )
    return chat


async def get_user_chats_async(
    limit: int, before_id: int | None, user: User, db: AsyncSession
) -> tuple[list[Chat], bool]:
    query = (
        select(Chat)
        .where(Chat.users.any(User.id == user.id))
        .order_by(desc(Chat.last_message_at), Chat.id)
        .limit(limit + 1)
    )
    if before_id is not None:
        query = query.where(Chat.id < before_id)
    result = await db.execute(query)
    chats = result.scalars().all()
    has_more = len(chats) > limit
    chats = chats[:limit]
    return chats, has_more


async def start_listening_async(ws: WebSocket, user: User, db: AsyncSession):
    await socket_manager.connect_socket_async(ws)
    logger.info("Websocket connection is established")
    await socket_manager.add_socket_connection_async(user.id, ws)
    if chat_ids := await get_user_chat_ids_async(user, db):
        for id in chat_ids:
            await socket_manager.add_user_to_channel_async(id, ws)
    else:
        chat_ids = {}
    return chat_ids


async def get_user_chat_ids_async(user: User, db: AsyncSession) -> set[int]:
    query = select(Chat.id).where(Chat.users.any(User.id == user.id))
    result = await db.execute(query)
    chats = result.scalars().all()
    return chats


@socket_manager.handler("new_message")
async def new_message_handle_async(
    data: dict,
    user: User,
    chat_ids: list[Chat],
    ws: WebSocket,
    db: AsyncSession,
    **kwargs,
):
    message = ReceiveMessage(**data)
    if not chat_ids or message.chat_id not in chat_ids:
        chat_ids.append(message.chat_id)
        await socket_manager.add_user_to_channel_async(message.chat_id, ws)
    new_message = Message(
        content=message.content, chat_id=message.chat_id, user_id=user.id
    )
    db.add(new_message)
    await db.flush()
    await db.refresh(new_message)
    chat = await db.get(Chat, new_message.chat_id)
    chat.last_message_at = new_message.created_at
    await db.commit()
    await db.refresh(chat)
    send_message = SendMessage(
        message_id=new_message.id,
        content=new_message.content,
        chat_id=new_message.chat_id,
        user_id=new_message.user_id,
        created_at=new_message.created_at,
    )
    outgoint_message = send_message.model_dump_json()
    await socket_manager.broadcast_to_channel_async(
        new_message.chat_id, outgoint_message
    )
