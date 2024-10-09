from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.message import Message
class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
    users: Mapped[list["User"]] = relationship(secondary="chat_participants", back_populates="chats")
    

