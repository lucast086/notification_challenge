from unittest.mock import AsyncMock, patch

import pytest

from app.core.exceptions import NotificationError
from app.schemas.notifications import NotificationUpdate
from app.services.notifications import NotificationService
from app.utils.mappers.notifications import toNotificationPrivate


def get_noti_list(notification):
    return [toNotificationPrivate(notification)]

@pytest.mark.asyncio
async def test_create_notification_success(get_valid_notification_db_info, get_noti_create, get_valid_user_db_info):
    with patch("app.services.notifications.STRATEGY_REGISTER") as mock_registry:
        mock_registry.get.return_value.return_value.send.return_value = {"status": "sent"}
        repo_mock = AsyncMock()
        repo_mock.create_or_update.return_value = get_valid_notification_db_info

        service = NotificationService(notification_repository=repo_mock)
        notification = await service.create(get_valid_user_db_info.id, get_noti_create)
        assert notification.id
        assert notification.tittle == get_noti_create.tittle
        assert notification.content == get_noti_create.content

@pytest.mark.asyncio
async def test_delete_notification_success(get_valid_notification_db_info):
    repo_mock = AsyncMock()
    repo_mock.get_by_id.return_value = get_valid_notification_db_info
    repo_mock.delete.return_value = None
    service = NotificationService(notification_repository=repo_mock)
    await service.delete(get_valid_notification_db_info.id)

    repo_mock.delete.assert_called_once_with(get_valid_notification_db_info.id)

@pytest.mark.asyncio
async def test_delete_notification_not_exists_error(get_valid_notification_db_info):
    repo_mock = AsyncMock()
    repo_mock.get_by_id.return_value = None
    repo_mock.delete.return_value = None
    service = NotificationService(notification_repository=repo_mock)
    with pytest.raises(NotificationError):
        await service.delete(get_valid_notification_db_info.id)

@pytest.mark.asyncio
async def test_update_notification_success(get_valid_notification_db_info):
    repo_mock = AsyncMock()
    repo_mock.get_by_id.return_value = get_valid_notification_db_info
    repo_mock.create_or_update.return_value = get_valid_notification_db_info

    get_valid_notification_db_info.tittle = "new tittle"
    data= NotificationUpdate(
        tittle="new tittle"
    )
    service = NotificationService(notification_repository=repo_mock)
    notification = await service.update(get_valid_notification_db_info.id, data)

    assert notification.tittle == data.tittle
    assert notification.id == get_valid_notification_db_info.id
    repo_mock.create_or_update.assert_called_once_with(get_valid_notification_db_info)

@pytest.mark.asyncio
async def test_update_notification_not_exists_error(get_valid_notification_db_info):
    repo_mock = AsyncMock()
    repo_mock.get_by_id.return_value = None
    repo_mock.update.return_value = None

    service = NotificationService(notification_repository=repo_mock)
    with pytest.raises(NotificationError):
        await service.update(get_valid_notification_db_info.id, NotificationUpdate())

@pytest.mark.asyncio
async def test_list_notification_empty_success(get_valid_user_db_info):
    repo_mock = AsyncMock()
    repo_mock.list.return_value = []
    service = NotificationService(notification_repository=repo_mock)
    results= await service.list(get_valid_user_db_info.id)

    assert results == []
    repo_mock.list.assert_called_once_with(user_id=get_valid_user_db_info.id)

@pytest.mark.asyncio
async def test_list_notification_success(get_valid_user_db_info, get_valid_notification_db_info):
    repo_mock = AsyncMock()
    repo_mock.list.return_value = [get_valid_notification_db_info]
    service = NotificationService(notification_repository=repo_mock)
    results= await service.list(get_valid_user_db_info.id)

    assert results == get_noti_list(get_valid_notification_db_info)
    repo_mock.list.assert_called_once_with(user_id=get_valid_user_db_info.id)