from fastapi import APIRouter, Depends, BackgroundTasks
from app.core.settings.app import AppSettings
from app.core.config import get_app_settings
import json

from app.api.types.models import User
from app.api.logic.user import create_token
from app.api.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.post("/create", name="users")
async def processing(input: User,
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        user_already_exist = await user_repo.select_user_by_email(
            email=input.email
        )

        if(user_already_exist): return {"user": "users email already exist" }

        user = await user_repo.create_user(
            username=input.username,
            email=input.email,
            password=input.password,
            token_api=create_token()
        )
        return {"user": user}
    except Exception as e:
        #TODO log error e
        print(e)
        return {"status": "Unexpected Error"}

@router.get("/", name="users")
async def processing(input: str,
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
