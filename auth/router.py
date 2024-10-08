from datetime import datetime, timezone
import logging
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Cookie, Depends, Response
from auth.service import (authenticate_async, create_access_token, create_refresh_token, refresh_access_token)
from db.database import get_db_async
from dependencies import get_current_user_async


logger = logging.getLogger(__name__)
auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/auth", summary="Create access and refresh token")
async def authenticate(response: Response, request: OAuth2PasswordRequestForm = Depends() ,db: AsyncSession = Depends(get_db_async)):
    user = await authenticate_async(request.username, request.password, db)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none",secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="none",secure=True)
    return {
        "name": user.name,
        "image_url": user.image_url
    }

@auth_router.get("/refresh", summary="Refresh access token")
async def refresh_access(response: Response, refresh_token: Annotated[str, Cookie()], db: AsyncSession = Depends(get_db_async)):
    access_token = await refresh_access_token(refresh_token, db)
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none",secure=True)
    return "Access token has been renewed"

@auth_router.get("/sign-out", summary="Sign out by removing cookies", dependencies=[Depends(get_current_user_async)])
async def sign_out(response: Response):
    expires = datetime.now(timezone.utc)
    response.set_cookie(
            key="access_token",
            value="",
            secure=True,
            httponly=True,
            samesite="none",
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )
    response.set_cookie(
            key="refresh_token",
            value="",
            secure=True,
            httponly=True,
            samesite="none",
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )
    return "Cookies removed"