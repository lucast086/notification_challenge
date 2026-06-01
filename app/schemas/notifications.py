from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class Channel(str, Enum):
      email = "email"
      sms = "sms"
      push = "push"


class NotificationBase(SQLModel):
    tittle: str
    content: str
    channel: Channel

class NotificationCreate(NotificationBase):
    recipient: Optional[str]  = None

class NotificationUpdate(BaseModel):
    tittle: Optional[str] = None
    content: Optional[str] = None
    channel: Optional[Channel] = None
    send_logs: Optional[Dict[str,Any]] = None
    recipient: Optional[str] = None

class NotificationPrivate(NotificationBase):
    id: int | None
    recipient: Optional[str]  = None
    send_logs: Optional[Dict[str,Any]] = None