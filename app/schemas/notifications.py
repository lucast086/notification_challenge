from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class Channel(str, Enum):
    """Supported delivery channels for notifications."""

    email = "email"
    sms = "sms"
    push = "push"


class NotificationBase(SQLModel):
    """Base schema with fields shared by all notification DTOs."""

    tittle: str
    content: str
    channel: Channel

class NotificationCreate(NotificationBase):
    """Schema for notification creation requests."""

    recipient: Optional[str]  = None

class NotificationUpdate(BaseModel):
    """Schema for partial notification update requests."""

    tittle: Optional[str] = None
    content: Optional[str] = None
    channel: Optional[Channel] = None
    send_logs: Optional[Dict[str,Any]] = None
    recipient: Optional[str] = None

class NotificationPrivate(NotificationBase):
    """Schema for notification data returned in API responses."""

    id: int | None
    recipient: Optional[str]  = None
    send_logs: Optional[Dict[str,Any]] = None