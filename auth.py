
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create access token
async def create_access_token(data: dict, expires_dalta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_dalta:
        expire = datetime.utcnow() + expires_dalta
    else: 
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return encoded_jwt

# Decode and verify token
async def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str =  payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None 