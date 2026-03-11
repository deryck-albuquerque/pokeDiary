import os

from datetime import datetime, timedelta, UTC
from typing import Any, Dict, Optional
from jose import JWTError, jwt

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Generate a JWT access token.
    :param data: payload data to include in the token.
    :return: encoded JWT token as string.
    """
    payload = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp": expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate and decode a JWT token.
    :param: token: JWT token.
    :return: decoded payload or None if token is invalid.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
