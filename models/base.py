from sqlalchemy import Column, DateTime, Integer


class Base():
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)