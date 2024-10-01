from sqlalchemy import Column, DateTime, Integer
from db.database import Base

class BaseEntity(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)