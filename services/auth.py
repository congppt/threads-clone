from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict
from jose import jwt, JWTError
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES"))

def gen_token(claims: dict[str, Any]):
    expired_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    claims.update({"exp": expired_at})
    return jwt.encode(claims, SECRET_KEY, ALGORITHM)

def get_claims(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, "HS256")
    except JWTError:
        raise