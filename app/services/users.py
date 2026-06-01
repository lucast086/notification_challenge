from typing import Annotated

from fastapi import Depends

import app.utils.mappers.users as userMapper
from app.core.exceptions import UserAlreadyExistsError
from app.models.users import User
from app.repositories.protocols import UserRepositoryProtocol
from app.repositories.users import UserRepository
from app.schemas.users import UserCreate, UserPublic


class UserService:


    def __init__(self, user_repository: Annotated[UserRepositoryProtocol, Depends(UserRepository)]) -> None:
        self.user_repository = user_repository

    async def create(self, user_create: UserCreate)-> UserPublic:
        """Register a new user after checking the email isn't already taken.

        Args:
            user_create: The registration data including email and password.

        Returns:
            The public representation of the newly created user.

        Raises:
            UserAlreadyExistsError: If a user with that email already exists.
        """
        
        user = await self.user_repository.get_by_email(user_create.email)
            
        if user:
            raise UserAlreadyExistsError(user)

        user = await self.user_repository.create(userMapper.toUser(user_create))
        return userMapper.toUserPublic(user)
