from datetime import datetime
from typing import Any, Dict

from app.models.notifications import Notification


class SendBySms:
    """Channel strategy that delivers notifications via SMS."""

    def send(self, notification: Notification) -> Dict[str, Any]:
        """Send a notification via SMS, truncating content to 160 characters.

        Args:
            notification: The notification object containing recipient and content.

        Returns:
            A dict with the delivery status, recipient number, and timestamp.
        """
        notification.content = notification.content[:160]
        return {
            "status": "sent",
            "content": notification.content,
            "recipient": notification.recipient,
            "sendend_at": datetime.now().isoformat(),
        }
