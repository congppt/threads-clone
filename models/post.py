from datetime import datetime
from db.database import Base
from models.user import User
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    content: Mapped[str | None]
    image_url: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    user: Mapped["User"] = relationship(back_populates="posts")
