from typing import Any, Dict, Protocol

from app.models.notifications import Notification


class SendStrategy(Protocol):
    """Protocol that all notification channel strategies must implement."""
    
    def send(self, notification: Notification) -> Dict[str,Any]:
        """Send a notification through the specific channel.

        Args:
            notification: The notification to be sent.

        Returns:
            A dict with the result of the send operation.
        """
        ...