
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Schema from user registration
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    fullname: Optional[str] = None

# Schema for user Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for updating user profile
class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    username: Optional[str] = None

# Schema for user response (what we send back)
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    fullname: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    email: Optional[str] = None

    