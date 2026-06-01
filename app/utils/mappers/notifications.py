from app.models.notifications import Notification
from app.schemas.notifications import NotificationCreate, NotificationPrivate


def toNotificationPrivate(notification: Notification)-> NotificationPrivate:
    """Map a Notification model to its public schema.

    Args:
        notification: The ORM model instance.

    Returns:
        A NotificationPrivate schema with the relevant fields.
    """
    return NotificationPrivate(
        id=notification.id,
        tittle=notification.tittle,
        content=notification.content,
        channel=notification.channel,
        send_logs=notification.send_logs,
        recipient=notification.recipient
        )

def toNotification(notification: NotificationCreate)-> Notification:
    """Map a NotificationCreate schema to the ORM Notification model.

    Args:
        notification: The creation schema with input data.

    Returns:
        A Notification model instance ready to be persisted.
    """
    return Notification(
        tittle=notification.tittle,
        content=notification.content,
        channel=notification.channel,
        recipient=notification.recipient
        )