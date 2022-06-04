from app.api.domain.common import DateTimeModelMixin, IDModelMixin
from app.api.domain.model import GenericModel
from app.api.services import security

class User(GenericModel):
    username: str
    email: str
    password: str
    token_api: str = ""


class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.hashed_password = security.get_password_hash("" + password)
        self.password = self.hashed_password
