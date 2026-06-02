
from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.dependencies.session import get_async_session
from app.models.users import User


class UserRepository():
    """Repository that handles all database operations for User entities.

    Attributes:
        session: The async database session used for queries.
    """

    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]) -> None:
        self.session = session
    
    async def create(self, user: User)-> User:
        """Persist a new user to the database.

        Args:
            user: The User instance to save.

        Returns:
            The saved User with its generated id populated.
        """
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user


    async def get_by_email(self, email: EmailStr)-> User:
        """Fetch a user by their email address.

        Args:
            email: The email to look up.

        Returns:
            The matching User, or None if not found.
        """
        statement = select(User).where(User.email== email)
        result =  await self.session.execute(statement=statement)
        return result.scalar_one_or_none()