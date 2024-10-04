from db.database import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from models.user import User
class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    content: Mapped[str]
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationships (if needed, can be added)
    from_user: Mapped["User"] = relationship(foreign_keys=[from_user_id], back_populates="sent_messages")
    to_user: Mapped["User"] = relationship(foreign_keys=[to_user_id], back_populates="received_messages")
