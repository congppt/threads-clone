from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    name = Column(String)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    imageUrl = Column(String, nullable=True)
    posts = relationship("Post", back_populates="posts")