from typing import Union
from fastapi import APIRouter, Depends, BackgroundTasks, Header, HTTPException
from app.core.settings.app import AppSettings
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from app.core.config import get_app_settings
import json
from app.api.services import jwt
from app.api.services import security

from app.api.types.models import User, UserUpdate
from app.api.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.post("/create", name="users:create")
async def create(input: User,
                 status_code=HTTP_201_CREATED,
                 settings: AppSettings = Depends(get_app_settings),
                 user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    user_already_exist = await user_repo.select_user_by_email(
        email=input.email
    )

    if(user_already_exist): return {"user": "users email already exist" }

    token = jwt.create_access_token_for_user(
        input,
        str(settings.secret_key),
    )

    user = await user_repo.create_user(
        username=input.username,
        email=input.email,
        password=input.password,
        token_api=token)

    return {"user": user, "status": HTTP_201_CREATED}

@router.get("/", name="users")
async def get_user(input: str,
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        user = await user_repo.select_user_by_email(
            email=input
        )
        return {"user": user}
    except Exception as e:
        #TODO log error e
        print(e)
        return {"status": "Unexpected Error"}
