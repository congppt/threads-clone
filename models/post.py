from sqlalchemy import Column, ForeignKey, Integer, String
from models.base_entity import BaseEntity
from sqlalchemy.orm import relationship


class Post(BaseEntity):
    __tablename__="posts"
    content = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user")