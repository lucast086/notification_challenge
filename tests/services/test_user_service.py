from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import UserAlreadyExistsError
from app.schemas.users import UserCreate
from app.services.users import UserService

user_create = UserCreate(
        email="somevalid@email.com",
        password='1!2P3s4',
        password_repeat='1!2P3s4'
    )

@pytest.mark.asyncio
async def test_create_user_success(get_valid_user_db_info):
    repo_mock = AsyncMock()
    repo_mock.get_by_email.return_value = None
    repo_mock.create.return_value = get_valid_user_db_info
    service = UserService(user_repository=repo_mock)
    user_public = await service.create(user_create)

    assert user_create.email == user_public.email



@pytest.mark.asyncio
async def test_create_user_exists_error(get_valid_user_db_info):
    repo_mock = AsyncMock()
    repo_mock.get_by_email.return_value = get_valid_user_db_info
    service = UserService(user_repository=repo_mock)

    with pytest.raises(UserAlreadyExistsError):
        await service.create(user_create) 


