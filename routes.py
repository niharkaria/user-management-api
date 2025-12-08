from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from database import get_db
from schemas import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from dependencies import get_current_active_user
from config import settings
import crud
import auth
from models import User

router = APIRouter()


# Register new user
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    print(f"Attempting to register: {user.email}")

    # Check email
    existing_user = await crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check username
    existing_username = await crud.get_user_by_username(db, username=user.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create new user
    new_user = await crud.create_user(db=db, user=user)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        username=new_user.username,
        created_at=new_user.created_at,
        is_active=new_user.is_active,
    )


# Login user
@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):

    # Get user
    user = await crud.get_user_by_email(db, email=user_credentials.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    valid = await auth.verify_password(user_credentials.password, user.hashed_password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check active
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is deactivated")

    # Create token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Get current profile
@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user=Depends(get_current_active_user)):
    return current_user


# Update user
@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):

    # Username check if changed
    if user_update.username:
        existing_user = await crud.get_user_by_username(db, username=user_update.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Username already taken")

    updated_user = await crud.update_user(db, user_id=current_user.id, user_update=user_update)
    return updated_user


# Deactivate account
@router.delete("/profile")
async def deactivate_account(
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    await crud.deactivate_user(db, user_id=current_user.id)
    return {"message": "Account deactivated successfully"}


# Get all users (async)
@router.get("/users")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
