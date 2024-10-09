from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import exists, select
from db.models.user import User
from user.schemas import UserProfile, UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from user.utils import hash

async def create_user_async(request: UserRegister, db: AsyncSession):
    query = select(exists().where(User.username == request.username))
    if (await db.execute(query)).scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exist!")
    user = User(name = request.name, username = request.username, hashed_password = hash(request.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
    
async def get_user_by_id_async(id: int, db: AsyncSession):
    query = select(User).where(User.id == id)
    try:
        user = (await db.execute(query)).scalar_one()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    
async def update_user_profile_async(request: UserProfile, user: dict[str, Any], db: AsyncSession):
    curr_user = await get_user_by_id_async(int(user["id"]), db)
    curr_user.name = request.name
    curr_user.image_url = request.image_url
    try:
        await db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"Profile not exist or accessible")