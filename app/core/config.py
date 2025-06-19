# app/core/config.py

import os
from pydantic_settings import BaseSettings

# To generate a new SECRET_KEY, you can run this in your terminal:
# openssl rand -hex 32

class Settings(BaseSettings):
    """
    Application settings are managed here using Pydantic's BaseSettings.
    """
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

# This line creates the 'settings' object that other files import.
# Make sure it's not misspelled and is outside the Settings class.
settings = Settings()