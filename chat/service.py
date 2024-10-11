from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload
from chat.schemas import ChatBase
from db.models.chat import Chat, ChatType
from db.models.message import Message
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

async def try_create_chat_async(request: ChatBase, user: User, db: AsyncSession) -> Chat:
    chat = None
    if len(request.user_ids) == 1:
        user_id = next(iter(request.user_ids))
        recipient = await __get_user_by_id_async(user_id)
        if recipient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not exist")
        chat = await try_get_direct_chat_async(user, recipient, db)
        if chat is not None:
            return chat
        chat = Chat(type = ChatType.DIRECT, name = request.name)
        chat.users.append(user)
        chat.users.append(recipient)      
    else:
        #not implemented
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

async def try_get_direct_chat_async(user: User, recipient: User, db: AsyncSession) -> Chat | None:
    query = select(Chat).where(Chat.type == ChatType.DIRECT, Chat.users.contains([user, recipient]))
    result = await db.execute(query)
    chat = result.scalar_one_or_none()
    return chat

async def get_chat_messages_async(id: int, limit: int, before_message_id: int | None, user: User, db: AsyncSession) -> tuple[list[Message], bool]:
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chat with id {id} does not exist")
    if user not in chat.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chat is not accessible")
    return chat

async def get_user_chats_async(limit: int, before_id: int | None, user: User, db: AsyncSession) -> tuple[list[Chat], bool]:
    query = select(Chat).where(user in Chat.users).order_by(desc(Chat.last_message_at)).limit(limit + 1)
    if before_id is not None:
        query = query.where(Chat.id < before_id)
    result = await db.execute(query)
    chats = result.scalars().all()
    has_more = len(chats) > limit
    chats = chats[:limit]
    return chats, has_more 
