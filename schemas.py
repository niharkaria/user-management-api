from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Schema for user registration
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for updating user profile
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None


# Schema for user response
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Token response schema
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data schema
class TokenData(BaseModel):
    email: Optional[str] = None
