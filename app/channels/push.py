from datetime import datetime
from typing import Any, Dict

from app.core.exceptions import DeviceTokenInvalid
from app.models.notifications import Notification


class SendByPush:
    """Channel strategy that delivers notifications via push notification."""

    def _device_token_is_valid(self):
        """Check whether the device token is valid."""
        # simulate token read and validation
        return True

    def _format_payload(self):
        """Format the push notification payload before sending."""
        # simulate some format
        pass

    def send(self, notification: Notification) -> Dict[str, Any]:
        """Send a notification via push.

        Args:
            notification: The notification object containing recipient token and content.

        Returns:
            A dict with the delivery status, recipient token, and timestamp.

        Raises:
            DeviceTokenInvalid: If the device token validation fails.
        """
        if not self._device_token_is_valid():
            raise DeviceTokenInvalid()

        self._format_payload()
        return {
            "status": "sent",
            "recipient": notification.recipient,
            "sendend_at": datetime.now().isoformat(),
        }
