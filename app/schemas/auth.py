from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class LoginCredentials(BaseModel):
    """Schema for login request payload."""

    email: EmailStr
    password: SecretStr


class Token(BaseModel):
    """Schema for the JWT token returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"
    expires_in: datetime