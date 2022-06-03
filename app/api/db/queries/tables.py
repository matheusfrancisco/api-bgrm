from datetime import datetime
from typing import Optional

from pypika import Parameter as CommonParameter, Query, Table

class Users(TypedTable):
    __table__ = "users"

    id: int
    username: str
    email: str
    password: str

users = Users()
