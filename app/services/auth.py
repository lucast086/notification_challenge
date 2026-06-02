
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Dict

import jwt
from fastapi import Depends
from passlib.context import CryptContext
from pydantic import SecretStr

from app.core.config import settings
from app.core.exceptions import UserOrPasswordError
from app.repositories.protocols import UserRepositoryProtocol
from app.repositories.users import UserRepository
from app.schemas.auth import LoginCredentials, Token


class AuthService:
    """Service that handles user authentication and JWT token generation.

    Attributes:
        hasher: bcrypt context used to hash and verify passwords.
        user_repository: Repository used to look up users by email.
    """

    hasher = CryptContext(schemes=["bcrypt"])

    def __init__(self, user_repository: Annotated[UserRepositoryProtocol, Depends(UserRepository)]) -> None:
        self.user_repository = user_repository
    
    def _create_access_token(self,data: Dict[str,Any])-> Token:
        """Build and sign a JWT access token with an expiration claim.

        Args:
            data: The payload to encode into the token (e.g. {"sub": email}).

        Returns:
            A Token schema with the encoded JWT and expiration datetime.
        """
        to_encode= data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        access_token = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)

        return Token(access_token=access_token, expires_in=expire)
    
    def _verify_password(self, password: SecretStr, hashed_password: str):
        """Compare a plain-text password against its bcrypt hash.

        Args:
            password: The plain-text password from the login request.
            hashed_password: The stored bcrypt hash to verify against.

        Returns:
            True if the password matches, False otherwise.
        """
        return self.hasher.verify(password.get_secret_value(),hashed_password)


    async def authenticate_user(self, loginData: LoginCredentials)-> Token:
        """Validate credentials and return a JWT token if they are correct.

        Args:
            loginData: The email and password submitted by the user.

        Returns:
            A Token with the signed JWT and its expiration.

        Raises:
            UserOrPasswordError: If the user doesn't exist or the password is wrong.
        """
        user = await self.user_repository.get_by_email(loginData.email)
        if not user or not self._verify_password(password=loginData.password, hashed_password= user.hashed_password):
            raise UserOrPasswordError(loginData.email)
        data={"sub": loginData.email}
        return self._create_access_token(data=data)