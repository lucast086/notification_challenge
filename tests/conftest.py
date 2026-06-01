from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr

from app.main import app
from app.models.notifications import Notification
from app.models.users import User
from app.schemas.auth import LoginCredentials
from app.schemas.notifications import Channel, NotificationCreate
from app.utils.functions import hash_password

basepath = "/v1"
password = SecretStr('1!2P3s4')

@pytest.fixture
def get_async_client():
    yield AsyncClient(transport=ASGITransport(app=app), base_url="https://test")

@pytest.fixture
def get_base_path():
    return basepath

@pytest.fixture
def get_valid_registration_data() -> dict[str,Any]:
    return {
        "email":"validemail@gmail.com",
        "password":"1!2P3s4",
        "password_repeat":"1!2P3s4"
        }

@pytest.fixture
def get_valid_user_db_info() -> User:
    
    return User(
        email="somevalid@email.com",
        hashed_password=hash_password(password),
        id=99
        )

@pytest.fixture
def get_valid_login_credentials() -> User:
    password = SecretStr('1!2P3s4')
    return LoginCredentials(
        email="somevalid@email.com",
        password=password)

@pytest.fixture
def get_invalid_login_credentials() -> User:
    password = SecretStr('12!23P33s43')
    return LoginCredentials(
        email="somevalid@email.com",
        password=password)

@pytest.fixture
def get_valid_notification_db_info() -> User:
    return Notification(
    id= 1,
    tittle='actual tittle',
    related_user= 1,
    send_logs= {},
    recipient='',
    channel=Channel.email,
    content='actual content'
    )

@pytest.fixture
def get_noti_create():
    return NotificationCreate(
    tittle='actual tittle',
    content='actual content',
    channel=Channel.email,
    recipient='')