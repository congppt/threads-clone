from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from chat import service
from chat.schemas import ChatBase, ChatDisplay, ChatMessage, ChatMessages
from db.database import get_db_async
from db.models.user import User
from dependencies import get_current_user_async


chat_router = APIRouter(prefix="/chat",  tags=["Chat"])

@chat_router.post("", response_model=ChatDisplay, summary="Create new chat (if not exist for direct type)")
async def try_create_chat_async(request: ChatBase, user: User = Depends(get_current_user_async), db: AsyncSession = Depends(get_db_async)):
    return await service.try_create_chat_async(request, user, db)

@chat_router.get("/{id}/messages", response_model=ChatMessages)
async def get_chat_messages_async(id: Annotated[int, Path(ge=1)], limit: Annotated[int, Query(10, ge=1)], before_message_id: Annotated[int | None, Query(None, ge=1)], user: User = Depends(get_db_async), db: AsyncSession = Depends(get_db_async)):
    messages, has_more = await service.get_chat_messages_async(id, limit, before_message_id, user, db)
    return ChatMessages(messages = messages, has_more = has_more)