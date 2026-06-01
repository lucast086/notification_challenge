from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import status

from app.core.exceptions import UserOrPasswordError
from app.main import app
from app.schemas.auth import Token
from app.services.auth import AuthService

mock_service = AsyncMock()
app.dependency_overrides[AuthService] = lambda: mock_service

@pytest.mark.asyncio
async def test_login_succesfull(get_base_path, get_valid_login_credentials, get_async_client):
    client = get_async_client
    url= get_base_path+"/auth/login"
    expected_response=Token(access_token="12345678", expires_in= datetime.now())
    mock_service.authenticate_user.return_value = expected_response
    mock_service.authenticate_user.return_status = status.HTTP_200_OK
    data= {
        "username":get_valid_login_credentials.email,
        "password":get_valid_login_credentials.password.get_secret_value()
    }
    async with client:
        response = await client.post(url=url, data=data)
    r = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token'in r and r['access_token'] != ''
    assert 'token_type' in r and r['token_type'] == 'bearer'
    assert 'expires_in' in r and r['expires_in'] != ''

@pytest.mark.asyncio
async def test_login_user_or_password_error(get_base_path, get_valid_login_credentials, get_async_client):
    client = get_async_client
    url= get_base_path+"/auth/login"
    expected_response= {"message":f'User with {get_valid_login_credentials.email} not exists, or password is incorrect'}
    mock_service.authenticate_user.side_effect = UserOrPasswordError(get_valid_login_credentials.email)
    data= {
        "username":get_valid_login_credentials.email,
        "password":get_valid_login_credentials.password.get_secret_value()
    }
    async with client:
        response = await client.post(url=url, data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response
