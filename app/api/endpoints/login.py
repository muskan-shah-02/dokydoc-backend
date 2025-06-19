from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api import deps
from app.db.base import FAKE_USERS_DB # Import from the new location

router = APIRouter()

# The FAKE_USERS_DB dictionary has been removed from this file.

@router.post("/users/", response_model=user_schema.User, status_code=201)
def create_user(*, user_in: user_schema.UserCreate) -> Any:
    """
    Create a new user.
    """
    user = FAKE_USERS_DB.get(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    
    hashed_password = get_password_hash(user_in.password)
    
    user_in_db = user_schema.UserInDB(
        **user_in.dict(exclude={"password"}), 
        id=len(FAKE_USERS_DB) + 1, 
        hashed_password=hashed_password
    )

    FAKE_USERS_DB[user_in.email] = user_in_db
    
    return user_in_db


@router.post("/login/access-token", response_model=token_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = FAKE_USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=user_schema.User)
def read_users_me(current_user: user_schema.User = Depends(deps.get_current_user)) -> Any:
    """
    Fetch the current logged in user.
    """
    return current_user

