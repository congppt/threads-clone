from datetime import datetime, timezone
from os import access
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exists, select
from db.database import get_db_async
from models.user import User
from dtos.user import UserDisplay, UserProfile, UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import gen_token
from utils import hash
from services.auth import oauth2_scheme, get_claims

async def create_user_async(request: UserRegister, db: AsyncSession):
    query = select(exists().where(User.username == request.username))
    if (await db.execute(query)).scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exist!")
    user = User(name = request.name, username = request.username, hashed_password = hash.hash(request.password), created_at = datetime.now(timezone.utc))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def auth_async(request: OAuth2PasswordRequestForm, db: AsyncSession):
    query = select(User).where(User.username == request.username)
    user = (await db.execute(query)).scalar()
    if user is None or not hash.is_correct_pwd(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username or password incorrect")
    access_token = gen_token({ "id" : user.id})
    return { "access_token" : access_token, "user" : UserDisplay.model_validate(user)}

async def get_current_user_async(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_async)):
    try:
        claims = get_claims(token)
        user_id = int(claims["id"])
        query = select(exists().where(User.id == user_id))
        if not (await db.execute(query)).scalar():
            raise
        return claims
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    
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