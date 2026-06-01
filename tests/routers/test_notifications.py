from unittest.mock import AsyncMock

import pytest
from fastapi import status

from app.core.exceptions import NotificationError
from app.dependencies.auth import get_current_user
from app.main import app
from app.schemas.notifications import Channel, NotificationPrivate
from app.services.notifications import NotificationService

mock_service = AsyncMock()
app.dependency_overrides[NotificationService] = lambda: mock_service

PROTECTED_ENDPOINTS = [
    ("GET", "/notifications"),
    ("POST", "/notifications"),
    ("DELETE", "/notifications/1"),
    ("PATCH", "/notifications/1"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("method,path", PROTECTED_ENDPOINTS)
async def test_endpoints_require_auth(get_base_path, get_async_client, method, path):
    client = get_async_client
    url = get_base_path + path
    async with client:
        response = await client.request(method=method, url=url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_list_notifications_successful(
    get_base_path,
    get_async_client,
    get_valid_user_db_info,
    get_valid_notification_db_info,
):
    app.dependency_overrides[get_current_user] = lambda: get_valid_user_db_info
    client = get_async_client
    url = get_base_path + "/notifications"
    expected = NotificationPrivate(
        id=get_valid_notification_db_info.id,
        tittle=get_valid_notification_db_info.tittle,
        content=get_valid_notification_db_info.content,
        channel=get_valid_notification_db_info.channel,
        recipient=get_valid_notification_db_info.recipient,
        send_logs=get_valid_notification_db_info.send_logs,
    )
    mock_service.list.return_value = [expected]

    async with client:
        response = await client.get(url=url)

    r = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(r, list)
    assert len(r) == 1
    assert r[0]["id"] == expected.id
    assert r[0]["tittle"] == expected.tittle

    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_create_notification_successful(
    get_base_path,
    get_async_client,
    get_valid_user_db_info,
    get_noti_create,
    get_valid_notification_db_info,
):
    app.dependency_overrides[get_current_user] = lambda: get_valid_user_db_info
    client = get_async_client
    url = get_base_path + "/notifications"
    expected = NotificationPrivate(
        id=get_valid_notification_db_info.id,
        tittle=get_noti_create.tittle,
        content=get_noti_create.content,
        channel=get_noti_create.channel,
        recipient=get_noti_create.recipient,
        send_logs={},
    )
    mock_service.create.return_value = expected

    async with client:
        response = await client.post(url=url, json=get_noti_create.model_dump())

    r = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert r["tittle"] == expected.tittle
    assert r["channel"] == expected.channel
    assert "id" in r

    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_delete_notification_successful(
    get_base_path,
    get_async_client,
    get_valid_user_db_info,
    get_valid_notification_db_info,
):
    app.dependency_overrides[get_current_user] = lambda: get_valid_user_db_info
    client = get_async_client
    notification_id = get_valid_notification_db_info.id
    url = get_base_path + f"/notifications/{notification_id}"
    mock_service.delete.return_value = None

    async with client:
        response = await client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_delete_notification_not_found(
    get_base_path, get_async_client, get_valid_user_db_info
):
    app.dependency_overrides[get_current_user] = lambda: get_valid_user_db_info
    client = get_async_client
    notification_id = 999
    url = get_base_path + f"/notifications/{notification_id}"
    mock_service.delete.side_effect = NotificationError(notification_id)

    async with client:
        response = await client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "message" in response.json()

    mock_service.delete.side_effect = None
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_update_notification_successful(
    get_base_path,
    get_async_client,
    get_valid_user_db_info,
    get_valid_notification_db_info,
):
    app.dependency_overrides[get_current_user] = lambda: get_valid_user_db_info
    client = get_async_client
    notification_id = get_valid_notification_db_info.id
    url = get_base_path + f"/notifications/{notification_id}"
    expected = NotificationPrivate(
        id=notification_id,
        tittle="updated tittle",
        content=get_valid_notification_db_info.content,
        channel=Channel.email,
        recipient=get_valid_notification_db_info.recipient,
        send_logs={},
    )
    mock_service.update.return_value = expected

    async with client:
        response = await client.patch(url=url, json={"tittle": "updated tittle"})

    r = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert r["tittle"] == "updated tittle"
    assert r["id"] == notification_id

    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_update_notification_not_found(
    get_base_path, get_async_client, get_valid_user_db_info
):
    app.dependency_overrides[get_current_user] = lambda: get_valid_user_db_info
    client = get_async_client
    notification_id = 999
    url = get_base_path + f"/notifications/{notification_id}"
    mock_service.update.side_effect = NotificationError(notification_id)

    async with client:
        response = await client.patch(url=url, json={"tittle": "new"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "message" in response.json()

    mock_service.update.side_effect = None
    app.dependency_overrides.pop(get_current_user, None)
