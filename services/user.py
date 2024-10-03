from datetime import datetime, timezone
from os import access
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exists, select
from models.user import User
from schemas import UserDisplay, UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import gen_token
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

async def auth(request: OAuth2PasswordRequestForm, db: AsyncSession):
    query = select(User).where(User.username == request.username)
    user = (await db.execute(query)).scalar()
    if user is None or not hash.is_correct_pwd(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username or password incorrect")
    access_token = gen_token({ "id" : user.id})
    return { "access_token" : access_token, "user" : UserDisplay.model_validate(user)}