from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    name: Mapped[str]
    username: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[bytes]
    image_url: Mapped[str | None]
    posts: Mapped[list["Post"]] = relationship(back_populates="user")