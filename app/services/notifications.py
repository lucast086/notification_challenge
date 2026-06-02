from typing import Annotated, Any, Dict

from fastapi import Depends
from sqlmodel import Integer

from app.channels import STRATEGY_REGISTER
from app.channels.protocols import SendStrategy
from app.core.exceptions import NotificationError
from app.models.notifications import Notification
from app.repositories.notifications import NotificationRepository
from app.repositories.protocols import NotificationRepositoryProtocol
from app.schemas.notifications import (
    NotificationCreate,
    NotificationPrivate,
    NotificationUpdate,
)
from app.utils.mappers import notifications as notificationMapper


class NotificationService():
    """Service that handles notification CRUD and channel dispatch logic.

    Attributes:
        notification_repository: Repository used to persist and query notifications.
    """

    def __init__(self, notification_repository: Annotated[NotificationRepositoryProtocol, Depends(NotificationRepository)]) -> None:
        self.notification_repository = notification_repository

    async def create(self, user_id: Integer, data: NotificationCreate)-> NotificationPrivate:
        """Create a notification and dispatch it through the appropriate channel.

        Args:
            user_id: The id of the user creating the notification.
            data: The payload with title, content, channel, and recipient.

        Returns:
            The created notification including send logs from the channel.
        """
        notification = notificationMapper.toNotification(data)
        notification.related_user = user_id
        
        strategy= STRATEGY_REGISTER.get(notification.channel)()
        
        send_logs = self.send_notification(notification, strategy)
        data_update = NotificationUpdate(send_logs=send_logs)
        notification = self._apply_update(notification, data_update)
        notification = await self.notification_repository.create_or_update(notification)

        return notificationMapper.toNotificationPrivate(notification)

    async def delete(self, notification_id : Integer):
        """Delete a notification by id, raising an error if it doesn't exist.

        Args:
            notification_id: The id of the notification to delete.

        Raises:
            NotificationError: If no notification with that id is found.
        """
        notification = await self.notification_repository.get_by_id(notification_id)

        if not notification:
            raise NotificationError(notification_id)
        return await self.notification_repository.delete(notification_id)

    async def update(self, notification_id : Integer, data:NotificationUpdate)-> NotificationPrivate:
        """Apply a partial update to an existing notification.

        Args:
            notification_id: The id of the notification to update.
            data: Fields to update; only set fields are applied.

        Returns:
            The updated notification.

        Raises:
            NotificationError: If no notification with that id is found.
        """
        notification = await self.notification_repository.get_by_id(notification_id)

        if not notification:
            raise NotificationError(notification_id)

        notification = self._apply_update(notification, data)
        notification = await self.notification_repository.create_or_update(notification)
        return notificationMapper.toNotificationPrivate(notification)

    async def list(self, user_id: Integer) -> list[NotificationPrivate]:
        """Return all notifications owned by a user.

        Args:
            user_id: The id of the user whose notifications to retrieve.

        Returns:
            A list of NotificationPrivate objects.
        """
        notification_list= await self.notification_repository.list(user_id=user_id)
        result:[NotificationPrivate] = []

        for noti in notification_list:
            result.append(notificationMapper.toNotificationPrivate(noti))
        
        return result

    def send_notification(self, notificacion: Notification, strategy: SendStrategy) -> Dict[str,Any]:
        """Delegate the send operation to the given channel strategy.

        Args:
            notificacion: The notification to send.
            strategy: The channel strategy to use (email, SMS, push).

        Returns:
            The send result logs returned by the strategy.
        """
        return strategy.send(notificacion)


    @staticmethod
    def _apply_update(notification: Notification, data: NotificationUpdate)-> Notification:
        """Merge update fields into a notification instance in place.

        Args:
            notification: The existing Notification to modify.
            data: The update schema; only explicitly set fields are applied.

        Returns:
            The same notification object with updated attributes.
        """

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(notification, k, v)
        
        return notification