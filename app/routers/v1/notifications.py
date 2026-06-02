from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.dependencies.auth import get_current_user
from app.models.users import User
from app.schemas.notifications import (
    NotificationCreate,
    NotificationPrivate,
    NotificationUpdate,
)
from app.services.notifications import NotificationService
from app.services.protocols import NotificationServiceProtocol
from app.swagger.notification_examples import create_notification_examples

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[NotificationPrivate]
)
async def list_notifications(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NotificationServiceProtocol, Depends(NotificationService)],
):
    """Return all notifications belonging to the authenticated user.

    Args:
        current_user: The user extracted from the JWT token.
        service: The notification service.

    Returns:
        A list of NotificationPrivate objects.
    """
    return await service.list(current_user.id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=NotificationPrivate
)
async def create_notification(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NotificationServiceProtocol, Depends(NotificationService)],
    data: NotificationCreate = Body(openapi_examples=create_notification_examples),
):
    """Create a new notification and dispatch it through the specified channel.

    Args:
        data: The notification payload with title, content, channel, and recipient.
        current_user: The user extracted from the JWT token.
        service: The notification service.

    Returns:
        The created NotificationPrivate including send logs.
    """
    return await service.create(current_user.id, data)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NotificationServiceProtocol, Depends(NotificationService)],
):
    """Delete a notification by id.

    Args:
        notification_id: The id of the notification to delete.
        current_user: The user extracted from the JWT token.
        service: The notification service.
    """
    return await service.delete(notification_id)


@router.patch(
    "/{notification_id}",
    status_code=status.HTTP_200_OK,
    response_model=NotificationPrivate,
)
async def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NotificationServiceProtocol, Depends(NotificationService)],
):
    """Partially update a notification.

    Args:
        notification_id: The id of the notification to update.
        data: Fields to update; unset fields are left unchanged.
        current_user: The user extracted from the JWT token.
        service: The notification service.

    Returns:
        The updated NotificationPrivate.
    """
    return await service.update(notification_id, data)
