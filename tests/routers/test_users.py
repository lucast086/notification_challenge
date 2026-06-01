from unittest.mock import AsyncMock

import pytest
from fastapi import status

from app.core.exceptions import UserAlreadyExistsError
from app.main import app
from app.schemas.users import UserPublic
from app.services.users import UserService

mock_service = AsyncMock()
app.dependency_overrides[UserService] = lambda: mock_service

@pytest.mark.asyncio
async def test_user_registration_succesfull(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    expected_response=UserPublic(email=get_valid_registration_data['email'])
    mock_service.create.return_value = expected_response
    mock_service.create.return_status = status.HTTP_201_CREATED

    async with client:
        response = await client.post(url=url, json=get_valid_registration_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response.model_dump()
    

@pytest.mark.asyncio
async def test_user_registration_with_already_registered_email(get_base_path, get_valid_registration_data, get_valid_user_db_info, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    expected_response={"message":f'User {get_valid_user_db_info.email} already exists'}
    mock_service.create.side_effect = UserAlreadyExistsError(get_valid_user_db_info)

    async with client:
        response = await client.post(url=url, json=get_valid_registration_data)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == expected_response



@pytest.mark.asyncio
async def test_user_registration_invalid_email(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    email_invalid={"email": "bademail",
    "password": get_valid_registration_data.get('password'),
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    async with client:
        response = await client.post(url=url, json=email_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {'detail': [{'field': 'email', 'message': 'value is not a valid email address: An email address must have an @-sign.'}]}

@pytest.mark.asyncio
async def test_user_registration_password_without_simbol(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={
        "email": get_valid_registration_data.get('email'),
        "password": "12345Ab",
        "password_repeat": get_valid_registration_data.get('password_repeat')
        }
    expected_response= {'detail': [{'field': 'password', 'message': "Value error, Password should have at least one of the symbols ['!', '#', '$', '%', '&', '(', ')', '*', '+', '-', '=', '@', '[', ']', '^', '_', '{', '}']"}]}

    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response

@pytest.mark.asyncio
async def test_user_registration_password_without_number(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={"email": get_valid_registration_data.get('email'),
    "password": "AbAbAb!",
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    expected_response= {'detail': [{'field': 'password', 'message': 'Value error, Password should have at least one numeral'}]}

    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response

@pytest.mark.asyncio
async def test_user_registration_password_without_lowercase(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={"email": get_valid_registration_data.get('email'),
    "password": "12345AB!",
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    expected_response = {'detail': [{'field': 'password', 'message': 'Value error, Password should have at least one lowercase letter'}]}
    
    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response

@pytest.mark.asyncio
async def test_user_registration_password_without_uppercase(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={"email": get_valid_registration_data.get('email'),
    "password": "12345ab!",
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    expected_response = {'detail': [{'field': 'password', 'message': 'Value error, Password should have at least one uppercase letter'}]}
    
    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response

@pytest.mark.asyncio
async def test_user_registration_password_without_minlength(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={"email": get_valid_registration_data.get('email'),
    "password": "1Ab!",
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    expected_response={'detail': [{'field': 'password', 'message': 'Value error, length should be at least 5 but not more than 20'}]}
    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response

@pytest.mark.asyncio
async def test_user_registration_password_without_maxlength(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={"email": get_valid_registration_data.get('email'),
    "password": "123456789123456789Ab!",
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    expected_response={'detail': [{'field': 'password', 'message': 'Value error, length should be at least 5 but not more than 20'}]}
    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response    

@pytest.mark.asyncio
async def test_user_registration_passwords_not_match(get_base_path, get_valid_registration_data, get_async_client):
    client = get_async_client
    url= get_base_path+"/users"
    password_invalid={"email": get_valid_registration_data.get('email'),
    "password": "123456Ab!",
    "password_repeat": get_valid_registration_data.get('password_repeat')}
    expected_response={'detail': [{'field': 'body', 'message': 'Value error, Passwords do not match'}]}
    async with client:
        response = await client.post(url=url, json=password_invalid)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == expected_response    
