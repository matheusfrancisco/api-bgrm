from os import environ

import pytest
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from app.api.db.repositories.users import UsersRepository
from app.api.domain.users import UserInDB
from tests.fake_asyncpg_pool import FakeAsyncPGPool

environ["APP_ENV"] = "test"

@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()

@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pool


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        app.state.pool = await FakeAsyncPGPool.create_pool(app.state.pool)
        yield app

@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client

@pytest.fixture
async def test_user(pool: Pool) -> UserInDB:
    async with pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            email="test@test.com", password="password", username="username"
        )
