from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import Integer, delete, select

from app.dependencies.session import get_async_session
from app.models.notifications import Notification


class NotificationRepository():
    """Repository that handles all database operations for Notification entities.

    Attributes:
        session: The async database session used for queries.
    """

    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]) -> None:
        self.session = session
    
    async def get_by_id(self, notification_id: Integer)-> Notification | None:
        """Fetch a notification by its primary key.

        Args:
            notification_id: The id of the notification to retrieve.

        Returns:
            The matching Notification, or None if not found.
        """
        statement = select(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none()

    async def create_or_update(self, notification: Notification)-> Notification:
        """Persist a new or existing notification.

        Args:
            notification: The Notification instance to save or update.

        Returns:
            The saved Notification with its current state refreshed from the DB.
        """
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)

        return notification

    async def delete(self, notification_id : Integer):
        """Delete a notification by its primary key.

        Args:
            notification_id: The id of the notification to remove.
        """
        statement = delete(Notification).where(Notification.id== notification_id)
        await self.session.execute(statement=statement)
        await self.session.commit()

    async def list(self, user_id: Integer) -> list[Notification]:
        """Return all notifications belonging to a given user.

        Args:
            user_id: The id of the user whose notifications to retrieve.

        Returns:
            A list of Notification objects for that user.
        """
        statement = select(Notification).where(Notification.related_user == user_id)       
        results = await self.session.execute(statement=statement)
        return results.scalars().all()
