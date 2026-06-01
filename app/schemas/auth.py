from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class LoginCredentials(BaseModel):
    email: EmailStr
    password: SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: datetime