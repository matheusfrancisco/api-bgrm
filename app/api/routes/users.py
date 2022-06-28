from typing import Union
from fastapi import APIRouter, Depends, BackgroundTasks, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api.services import security
from app.api.domain.users import UserInDB
from app.core.settings.app import AppSettings
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from app.core.config import get_app_settings
import json
from app.api.services import jwt

from app.api.types.models import User
from app.api.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login", response_model=jwt.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                settings: AppSettings = Depends(get_app_settings),
                                user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    user = await security.authenticate_user(form_data.username, form_data.password, user_repo)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt.create_access_token_for_user(form_data, settings.secret_key)
    return {"access_token": access_token, "token_type": "bearer"}

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
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
                     token: str = Depends(oauth2_scheme)):
    try:
        user = await user_repo.select_user_by_email(
            email=input
        )
        return {"user": user}
    except Exception as e:
        #TODO log error e
        print(e)
        return {"status": "Unexpected Error"}
