from datetime import datetime, timedelta, timezone
import os
from typing import Any
from bcrypt import checkpw, hashpw, gensalt
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES"))
REFRESH_TOKEN_MINUTES = int(os.getenv("REFRESH_TOKEN_MINUTES"))

def hash(pwd: str) -> str:
    return hashpw(pwd.encode(), gensalt())

def is_correct_pwd(pwd: str, hashed_pwd: bytes):
    return checkpw(pwd.encode(), hashed_pwd)

def gen_access_token(claims: dict[str, Any]):
    return __gen_token(claims, ACCESS_TOKEN_MINUTES)

def gen_refresh_token(claims: dict[str, Any]):
    return __gen_token(claims, REFRESH_TOKEN_MINUTES)

def __gen_token(claims: dict[str, Any], minutes: int):
    expired_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    claims.update({"exp": expired_at})
    return jwt.encode(claims, SECRET_KEY, ALGORITHM)

def get_claims(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, "HS256")
    except ExpiredSignatureError:
        raise Exception("Signature expired")
    except JWTClaimsError:
        raise Exception("Cannot resolve identity")
    except JWTError:
        raise Exception("Cannot resolve identity")