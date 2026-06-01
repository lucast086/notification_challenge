from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import LoginCredentials, Token
from app.services.auth import AuthService
from app.services.protocols import AuthServiceProtocol

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: Annotated[AuthServiceProtocol, Depends(AuthService)]):
    """Authenticate a user and return a JWT access token.

    Args:
        form_data: OAuth2 form with username (email) and password.
        service: The auth service handling credential validation.

    Returns:
        A Token with the signed JWT and expiration info.
    """
    login_credentials=LoginCredentials(
        email=form_data.username,password=form_data.password
    )
    
    return await service.authenticate_user(login_credentials)
