from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict
from jose import jwt, JWTError
from fastapi import Depends
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES"))

def gen_token(claims: Dict[str, Any]):
    expired_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    claims.update({"exp": expired_at})
    return jwt.encode(claims, SECRET_KEY, ALGORITHM)

def get_claims(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, "HS256")
    except JWTError:
        raise