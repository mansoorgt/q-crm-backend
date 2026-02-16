from datetime import datetime, timedelta
from typing import Any, Union
import hashlib
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

PROMETHEUS_SETTINGS = {
    "SECRET_KEY": settings.SECRET_KEY, 
    "ALGORITHM": settings.ALGORITHM
}

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_password = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256_password, hashed_password)

def get_password_hash(password: str) -> str:
    sha256_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha256_password)

