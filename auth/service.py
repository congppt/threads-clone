from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth import utils
from db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

async def authenticate_async(username: str, password: str, db: AsyncSession) -> User:
    user = await _get_user_by_username_async(username, db)
    if user is None or not utils.is_correct_pwd(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Password or username incorrect")
    return user

async def _get_user_by_username_async(username: str, db: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar()
    return user

async def refresh_access_token_async(refresh_token: str, db: AsyncSession) -> str:
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    
    try:
        payload= utils.get_claims(refresh_token)    
    except Exception as e:
        creds_exception.detail = str(e)
        raise creds_exception
    
    username = payload.get("username")
    if username is None:
        raise creds_exception
    
    user = await _get_user_by_username_async(payload["username"], db)
    if user is None:
        raise creds_exception
    access_token = gen_access_token(user)
    return access_token

def gen_access_token(user: User) -> str:
    claims = { "id": user.id, "username": user.username }
    return utils.gen_access_token(claims)

def gen_refresh_token(user: User) -> str:
    claims = { "username": user.username }
    return utils.gen_refresh_token(claims)