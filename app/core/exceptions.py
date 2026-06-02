
from fastapi import status
from pydantic import EmailStr
from sqlmodel import Integer

from app.models.users import User


class DomainError(Exception):
    """Base class for all domain-level exceptions in this application."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UserAlreadyExistsError(DomainError):
    """Raised when attempting to register a user with an email that is already taken."""

    def __init__(self, user: User) -> None:
        email=  user.email
        self.status_code= status.HTTP_409_CONFLICT
        self.message = f'User {email} already exists'
        super().__init__(self.message, self.status_code)

class UserOrPasswordError(DomainError):
    """Raised when the email does not exist or the password does not match."""

    def __init__(self, email: EmailStr) -> None:
        self.status_code= status.HTTP_404_NOT_FOUND
        self.message = f'User with {email} not exists, or password is incorrect'
        super().__init__(self.message, self.status_code)

class CredentialsException(DomainError):
    """Raised when a JWT token cannot be validated."""

    def __init__(self) -> None:
        self.status_code= status.HTTP_401_UNAUTHORIZED
        self.message = "Could not validate credentials"
        super().__init__(self.message, self.status_code)

class NotificationError(DomainError):
    """Raised when a notification with the given id does not exist."""

    def __init__(self, id: Integer) -> None:
        self.status_code= status.HTTP_404_NOT_FOUND
        self.message = f'Notification with {id} not exists'
        super().__init__(self.message, self.status_code)

class DeviceTokenInvalid(DomainError):
    """Raised when the push notification device token fails validation."""

    def __init__(self) -> None:
        self.status_code= status.HTTP_400_BAD_REQUEST
        self.message = "Could not validate device token"
        super().__init__(self.message, self.status_code)


class InvalidRecipient(DomainError):
    """Raised when the notification recipient fails format validation."""

    def __init__(self) -> None:
        self.status_code= status.HTTP_400_BAD_REQUEST
        self.message = "Could not validate recipient"
        super().__init__(self.message, self.status_code)