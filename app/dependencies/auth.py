from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.exceptions import CredentialsException
from app.repositories.protocols import UserRepositoryProtocol
from app.repositories.users import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],user_repository: Annotated[UserRepositoryProtocol, Depends(UserRepository)]):
    """Decode the JWT token and return the authenticated user.

    Args:
        token: The Bearer token extracted from the Authorization header.
        user_repository: Repository used to look up the user by email.

    Returns:
        The User instance associated with the token's subject claim.

    Raises:
        CredentialsException: If the token is invalid, expired, or the user doesn't exist.
    """

    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value() , algorithms=[settings.algorithm])
        email = payload.get("sub")
        if email is None:
            raise CredentialsException()
    except jwt.InvalidTokenError:
        raise CredentialsException()
    user = user_repository.get_by_email(email=email)
    if user is None:
        raise CredentialsException()
    return user