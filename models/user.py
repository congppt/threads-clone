from sqlalchemy import Column, DateTime, Integer, LargeBinary, String
from sqlalchemy.orm import relationship
from db.database import Base
from models import post

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True))
    name = Column(String)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(LargeBinary)
    imageUrl = Column(String, nullable=True)
    posts = relationship("Post", back_populates="user")