from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.schemas.users import UserCreate, UserPublic
from app.services.protocols import UserServiceProtocol
from app.services.users import UserService
from app.swagger.user_examples import register_examples

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def user_registration(
    service: Annotated[UserServiceProtocol, Depends(UserService)],
    userData: UserCreate = Body(
        openapi_examples=register_examples,
    ),
):
    """Register a new user account.

    Args:
        userData: Registration payload with email and password.
        service: The user service handling the creation logic.

    Returns:
        The public profile of the newly registered user.
    """
    return await service.create(userData)
