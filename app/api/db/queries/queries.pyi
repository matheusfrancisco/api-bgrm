from typing import Dict, Optional, Sequence
from asyncpg import Connection

class UsersQueriesMixin:
    async def create_new_user(
            self,
            conn: Connection,
            *,
            username: str,
            email: str,
            password: str,
    ) -> Record: ...

    async def select_user_by_teacher_code(
            self,
            conn: Connection,
            *,
            email: str,
    ) -> Record: ...

    async def select_user_by_username(
            self,
            conn: Connection,
            *,
            username: str,
    ) -> Record: ...

class Queries(
    UsersQueriesMixin,
): ...

queries: Queries
