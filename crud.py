from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from schemas import UserCreate, UserUpdate
from auth import hash_password

# Create new user
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_pwd = await hash_password(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pwd,
        full_name=user.full_name
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


# Get user by email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


# Get user by username
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


# Get user by ID
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


# Update user profile
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    user_in_db = await get_user_by_id(db, user_id)
    if not user_in_db:
        return None

    if user_update.full_name is not None:
        user_in_db.full_name = user_update.full_name
    if user_update.username is not None:
        user_in_db.username = user_update.username

    await db.commit()
    await db.refresh(user_in_db)

    return user_in_db


# Deactivate user
async def deactivate_user(db: AsyncSession, user_id: int):
    user_in_db = await get_user_by_id(db, user_id)
    if not user_in_db:
        return None

    user_in_db.is_active = False

    await db.commit()
    await db.refresh(user_in_db)

    return user_in_db
