from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.core.config import settings
from app.schemas import token as token_schema
from app.schemas import user as user_schema
from app.db.base import FAKE_USERS_DB # Import from the new, correct location

# This tells FastAPI which URL to use to get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> user_schema.User:
    """
    Dependency function to decode a JWT token and get the current user.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = token_schema.TokenData(email=payload.get("sub"))
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = FAKE_USERS_DB.get(token_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

