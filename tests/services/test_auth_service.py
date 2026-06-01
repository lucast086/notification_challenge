from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest

from app.core.config import settings
from app.core.exceptions import UserOrPasswordError
from app.services.auth import AuthService


@pytest.mark.asyncio
async def test_authenticate_user_success(get_valid_user_db_info, get_valid_login_credentials):
    repo_mock = AsyncMock()
    repo_mock.get_by_email.return_value = get_valid_user_db_info

    service = AuthService(user_repository=repo_mock)

    token = await service.authenticate_user(get_valid_login_credentials)

    decoded_token = jwt.decode(token.access_token, settings.secret_key.get_secret_value(), settings.algorithm)
    assert "exp" in decoded_token
    assert "sub" in decoded_token
    assert get_valid_login_credentials.email == decoded_token.get('sub')

@pytest.mark.asyncio
async def test_authenticate_user_not_exist_error(get_valid_login_credentials):
    repo_mock = AsyncMock()
    repo_mock.get_by_email.return_value = None

    service = AuthService(user_repository=repo_mock)

    with pytest.raises(UserOrPasswordError):
        await service.authenticate_user(get_valid_login_credentials)


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password_error(get_valid_user_db_info, get_invalid_login_credentials):
    repo_mock = AsyncMock()
    repo_mock.get_by_email.return_value = get_valid_user_db_info

    service = AuthService(user_repository=repo_mock)

    with pytest.raises(UserOrPasswordError):
        await service.authenticate_user(get_invalid_login_credentials)

def test_create_access_token():
    data={"sub": "somevalid@email.com"}
    repo_mock = MagicMock()

    service = AuthService(user_repository=repo_mock)

    token = service._create_access_token(data=data)
    
    decoded_token = jwt.decode(token.access_token, settings.secret_key.get_secret_value(), settings.algorithm)
    assert "exp" in decoded_token
    assert "sub" in decoded_token
    assert data["sub"] == decoded_token.get('sub')
