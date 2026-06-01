
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.users import UserCreate, UserPublic
from app.services.protocols import UserServiceProtocol
from app.services.users import UserService

router = APIRouter(prefix='/users', tags=["users"])

@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def user_registration(userData: UserCreate, service: Annotated[UserServiceProtocol, Depends(UserService)]):
    """Register a new user account.

    Args:
        userData: Registration payload with email and password.
        service: The user service handling the creation logic.

    Returns:
        The public profile of the newly registered user.
    """
    return await service.create(userData)
    