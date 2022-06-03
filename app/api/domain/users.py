from app.api.domain.common import DateTimeModelMixin, IDModelMixin
from app.api.domain.model import GenericModel

class User(GenericModel):
    username: str
    email: str
    password: str
    token_api: str


class UserInDB(IDModelMixin, DateTimeModelMixin, User): ...
