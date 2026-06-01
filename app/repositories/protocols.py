from typing import Protocol

from pydantic import EmailStr
from sqlmodel import Integer

from app.models.notifications import Notification
from app.models.users import User


class UserRepositoryProtocol(Protocol):

    async def create(self, user: User)-> User:
        pass

    async def get_by_email(self, email: EmailStr)-> User:
        pass

class NotificationRepositoryProtocol(Protocol):

    async def get_by_id(self, notification_id: Integer)-> Notification | None:
        pass

    async def create_or_update(self, user_id: Integer, data: Notification)-> Notification:
        pass

    async def delete(self, notification_id : Integer):
        pass

    async def update(self, notification_id : Integer, data:Notification)-> Notification:
        pass

    async def list(self, user_id: Integer) -> list[Notification]:
        pass