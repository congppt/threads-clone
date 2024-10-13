from datetime import datetime
import enum
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Enum
from db.models.message import Message

class ChatType(enum.Enum):
    DIRECT = "direct"
    GROUP = "group"
class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str] = mapped_column(Enum(ChatType))
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
    last_message_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.min)
    users: Mapped[list["User"]] = relationship(secondary="chat_participants", back_populates="chats")
    

