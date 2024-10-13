import os
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from db.models import *

DATABASE_URL = os.getenv("DATABASE")
REDIS_URL = os.getenv("REDIS")
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Prevent objects from being expired after commit
)

Base = declarative_base()

async def get_db_async():
    try:
        async with AsyncSession() as session:
            yield session
    except:
        await session.rollback()
        raise

def create_redis_pool():
    return ConnectionPool.from_url(REDIS_URL)

redis_pool = create_redis_pool()

def get_cache():
    return Redis(connection_pool=redis_pool)