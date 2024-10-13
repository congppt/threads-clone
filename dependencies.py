from typing import Annotated
from fastapi import Cookie, Depends, HTTPException, status
from auth import utils
from db.database import get_db_async
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from auth.service import _get_user_by_username_async

async def get_current_user_async(access_token: Annotated[str | None, Cookie()], db: AsyncSession = Depends(get_db_async)) -> User:
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    
    try:
        payload= utils.get_claims(access_token)    
    except Exception as e:
        creds_exception.detail = str(e)
        raise creds_exception
    
    username = payload.get("username")
    if not username:
        raise creds_exception
    
    user = await _get_user_by_username_async(username)
    if not user:
        raise creds_exception
    return user

