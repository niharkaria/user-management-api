
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate
from auth import hash_password

# Create new user
async def create_user(db:Session, user: UserCreate):
    hash_pwd = hash_password(user.password)
    db_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hash_pwd,
        full_name = user.fullname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email
async def get_user_by_email(db: Session, email:str):
    return db.query(User).filter(User.email == email).first()

# Get user by username
async def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username ==  username).first()

# Get user by ID
async def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id ==  user_id).first()

# Update user profile
async def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # Update only provided fields
    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name
    if user_update.username is not None:
        db_user.username = user_update.username

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete (deactivate) user
async def deactivate_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user