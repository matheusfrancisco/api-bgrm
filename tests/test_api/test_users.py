import pytest
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.api.db.repositories.users import UsersRepository
from app.api.domain.users import UserInDB

pytestmark = pytest.mark.asyncio

async def test_user_success_registration(
    app: FastAPI, client: AsyncClient, pool: Pool
) -> None:
    email, username, password = "test@test.com", "username", "password"
    registration_json = {
      "email": email, "username": username, "password": password
    }

    response = await client.post(
        app.url_path_for("users:create"), json=registration_json
    )

    r = response.json()
    u = r.get("user")

    udb = UserInDB(
        username= u.get("username"),
        email=u.get("email"),
        password=u.get("password"),
        hashed_password=u.get("password"),
    )

    assert r["status"] == HTTP_201_CREATED
    assert udb.email == email
    assert udb.username == username
    assert udb.check_password(password)
