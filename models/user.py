from sqlalchemy import Column, String
from models.base_entity import BaseEntity
from sqlalchemy.orm import relationship

class User(BaseEntity):
    __tablename__="users"
    name = Column(String),
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    imageUrl = Column(String, nullable=True)
    posts = relationship("Post", back_populates="posts")