from typing import Any, Dict, Protocol

from sqlmodel import Integer

from app.models.users import User
from app.schemas.auth import LoginCredentials, Token
from app.schemas.notifications import (
    NotificationCreate,
    NotificationPrivate,
    NotificationUpdate,
)
from app.schemas.users import UserCreate, UserPublic


class UserServiceProtocol(Protocol):
    """Protocol defining the interface for user service operations."""

    async def create(self, user: UserCreate)-> UserPublic:
        """Register a new user and return their public representation."""
        pass


class AuthServiceProtocol(Protocol):
    """Protocol defining the interface for authentication service operations."""

    async def authenticate_user(self, loginData: LoginCredentials)-> Token:
        """Validate credentials and return a signed JWT token."""
        pass

class NotificationServiceProtocol(Protocol):
    """Protocol defining the interface for notification service operations."""

    async def create(self, user_id: Integer, data: NotificationCreate)-> NotificationPrivate:
        """Create a notification and dispatch it through the appropriate channel."""
        pass

    async def delete(self, notification_id : Integer):
        """Delete the notification with the given id."""
        pass

    async def update(self, notification_id : Integer, data:NotificationUpdate)-> NotificationPrivate:
        """Apply a partial update to an existing notification."""
        pass

    async def list(self, user_id: Integer) -> list[NotificationPrivate]:
        """Return all notifications owned by the given user."""
        pass