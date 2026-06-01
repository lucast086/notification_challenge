
from fastapi import status
from pydantic import EmailStr
from sqlmodel import Integer

from app.models.users import User


class DomainError(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserAlreadyExistsError(DomainError):

    def __init__(self, user: User) -> None:
        email=  user.email
        self.status_code= status.HTTP_409_CONFLICT
        self.message = f'User {email} already exists'
        super().__init__(self.message, self.status_code)

class UserOrPasswordError(DomainError):

    def __init__(self, email: EmailStr) -> None:
        self.status_code= status.HTTP_404_NOT_FOUND
        self.message = f'User with {email} not exists, or password is incorrect'
        super().__init__(self.message, self.status_code)

class CredentialsException(DomainError):

    def __init__(self) -> None:
        self.status_code= status.HTTP_401_UNAUTHORIZED
        self.message = "Could not validate credentials"
        super().__init__(self.message, self.status_code)

class NotificationError(DomainError):

    def __init__(self, id: Integer) -> None:
        self.status_code= status.HTTP_404_NOT_FOUND
        self.message = f'Notification with {id} not exists'
        super().__init__(self.message, self.status_code)

class DeviceTokenInvalid(DomainError):
    def __init__(self) -> None:
        self.status_code= status.HTTP_400_BAD_REQUEST
        self.message = "Could not validate device token"
        super().__init__(self.message, self.status_code)


class InvalidRecipient(DomainError):
    def __init__(self) -> None:
        self.status_code= status.HTTP_400_BAD_REQUEST
        self.message = "Could not validate recipient"
        super().__init__(self.message, self.status_code)