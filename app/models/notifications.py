from typing import Any, Dict, Optional

from sqlmodel import JSON, Field

from app.schemas.notifications import NotificationBase


class Notification(NotificationBase, table=True):
    """Database model representing a notification owned by a user."""
    id: int | None = Field(default=None, primary_key=True)
    related_user: int | None = Field(default=None, foreign_key="user.id")
    send_logs: Dict[str,Any] | None = Field(default= {"status": "pending"}, sa_type=JSON)
    recipient: Optional[str]
    