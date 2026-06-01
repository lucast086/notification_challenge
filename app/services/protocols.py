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

    async def create(self, user: UserCreate)-> UserPublic:
        pass


class AuthServiceProtocol(Protocol):

    async def authenticate_user(self, loginData: LoginCredentials)-> Token:
        pass

class NotificationServiceProtocol(Protocol):

    async def create(self, user_id: Integer, data: NotificationCreate)-> NotificationPrivate:
        pass

    async def delete(self, notification_id : Integer):
        pass

    async def update(self, notification_id : Integer, data:NotificationUpdate)-> NotificationPrivate:
        pass

    async def list(self, user_id: Integer) -> list[NotificationPrivate]:
        pass