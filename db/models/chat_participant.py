from sqlalchemy import ForeignKey
from db.database import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    # user: Mapped["User"] = relationship(back_populates="chats")
    # chats: Mapped["Chat"] = relationship(back_populates="users")