from typing import Optional, Union, Any

from app.api.db.queries.queries import queries
from app.api.db.repositories.base import BaseRepository
from app.api.domain.users import User, UserInDB


class UsersRepository(BaseRepository):
    async def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
        token_api: str,
    ) -> UserInDB:
        user = UserInDB(
            username=username,
            email=email,
            password=password,
            token_api=token_api)

        async with self.connection.transaction():
            user_row = await queries.create_new_user(
                self.connection,
                username=user.username,
                email=user.email,
                token_api=user.token_api,
                password=user.password
            )

        return user.copy(update=dict(user_row))


    async def select_user_by_email(self, *, email: str,) -> Union[Any]:
        user_row = await queries.select_user_by_teacher_code(
            self.connection,
            email=email)

        if len(user_row) > 0:
            return user_row[0]
        return None
