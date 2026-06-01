from datetime import datetime
from typing import Any, Dict

from email_validator import EmailNotValidError, validate_email

from app.core.exceptions import InvalidRecipient
from app.models.notifications import Notification


class SendByEmail():

    def _recipient_format_is_valid(self, email:str):
        """Check whether the recipient email address has a valid Sformat."""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    def _generate_template(self):
        """Build the email template for the notification."""
        #simulate template generation
        pass

    def send(self, notification: Notification) -> Dict[str,Any]:
        """Send a notification via email.

        Args:
            notification: The notification object containing recipient and content.

        Returns:
            A dict with the delivery status, recipient address, and timestamp.

        Raises:
            InvalidRecipient: If the recipient format validation fails.
        """
        if not self._recipient_format_is_valid(notification.recipient):
            raise InvalidRecipient()
        self._generate_template()

        return {
            "status": "sent",
            "recipient": notification.recipient,
            "sendend_at": datetime.now()
        }