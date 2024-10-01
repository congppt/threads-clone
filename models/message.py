from sqlalchemy import Column, ForeignKey, Integer, String
from models.base_entity import BaseEntity
from sqlalchemy.orm import relationship

class Message(BaseEntity):
    __tablename__="messages"
    content = Column(String)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
