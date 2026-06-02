from typing import Protocol

from pydantic import EmailStr
from sqlmodel import Integer

from app.models.notifications import Notification
from app.models.users import User


class UserRepositoryProtocol(Protocol):
    """Protocol defining the interface for user persistence operations."""

    async def create(self, user: User)-> User:
        """Persist a new user and return it with its generated id."""
        pass

    async def get_by_email(self, email: EmailStr)-> User:
        """Return the user matching the given email, or None if not found."""
        pass

class NotificationRepositoryProtocol(Protocol):
    """Protocol defining the interface for notification persistence operations."""

    async def get_by_id(self, notification_id: Integer)-> Notification | None:
        """Return the notification with the given id, or None if not found."""
        pass

    async def create_or_update(self, user_id: Integer, data: Notification)-> Notification:
        """Persist a new or existing notification and return the refreshed instance."""
        pass

    async def delete(self, notification_id : Integer):
        """Remove the notification with the given id from the database."""
        pass

    async def update(self, notification_id : Integer, data:Notification)-> Notification:
        """Apply updates to an existing notification and return the updated instance."""
        pass

    async def list(self, user_id: Integer) -> list[Notification]:
        """Return all notifications belonging to the given user."""
        pass