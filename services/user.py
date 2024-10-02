from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy import exists, select
from models.user import User
from schemas import UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from utils import hash

async def create_user(request: UserRegister, db: AsyncSession):
    query = select(exists().where(User.username == request.username))
    if (await db.execute(query)).scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exist!")
    user = User(name = request.name, username = request.username, hashed_password = hash.hash(request.password), created_at = datetime.now(timezone.utc))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user