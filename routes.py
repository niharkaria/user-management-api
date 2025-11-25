
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from schemas import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from dependencies import get_current_active_user
from config import settings
import crud
import auth

router = APIRouter()

# Register new user
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Attempting to register: {user.email}")
    
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        print(f"Email {user.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = crud.get_user_by_username(db, username=user.username)
    if existing_username:
        print(f"Username {user.username} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    print("Creating new user...")
    new_user = crud.create_user(db=db, user=user)
    print(f"User created successfully: {new_user.email}")
    return new_user

# Login user
@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Get user by email
    user = crud.get_user_by_email(db, email=user_credentials.email)

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invaild credentials"
        )
    
    # verify password
    if not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaild credentials"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated"
        )
    
    # Checks access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta = access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Get current user profile
@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user = Depends(get_current_active_user)):
    return current_user

# Update user profile
@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update = UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # If username is being updated, check if it's already taken
    if user_update.username:
        existing_user = crud.get_user_by_username(db, username=user_update.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
    # Update user
    updated_user = crud.update_user(db, user_id=current_user.id, user_update=user_update)
    return updated_user

# Deactivate account
@router.delete("/profile")
async def deactivate_account(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crud.deactivate_user(db, user_id=current_user.id)
    return {"message": "Account deactivated successfully"}

# Get all users (for testing only - remove in production!)
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    from models import User  # Import User model
    users = db.query(User).all()  # Correct!
    return users