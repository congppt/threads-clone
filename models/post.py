from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    content = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user")