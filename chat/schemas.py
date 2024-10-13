from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uvicorn import Config
from db.models.chat import ChatType

class ChatBase(BaseModel):
    user_ids: set[int]
    name: str | None

class ChatDisplay(BaseModel):
    id : int
    name: str | None
    type: ChatType
    model_config = ConfigDict(from_attributes=True)

class MessageDisplay(BaseModel):
    id: int
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ChatMessages(BaseModel):
    messages: list[MessageDisplay]
    has_more: bool
    model_config = ConfigDict(from_attributes=True)

class ChatPage(BaseModel):
    chats: list[ChatDisplay]
    has_more: bool
    model_config = ConfigDict(from_attributes=True)

class ReceiveMessage(BaseModel):
    chat_id: int
    content: str

class SendMessage(BaseModel):
    type: str = "new"
    message_id: int
    chat_id: int
    user_id: int
    content: str
    created_at: datetime

