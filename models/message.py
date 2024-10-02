from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from db.database import Base

class Message(Base):
    __tablename__="messages"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True))
    content = Column(String)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
