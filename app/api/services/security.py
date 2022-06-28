import bcrypt
from passlib.context import CryptContext

from app.api.db.repositories.users import UsersRepository
from app.api.services import security

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str,
                            user_repo: UsersRepository):
    user = await user_repo.select_user_by_username(username=username)
    if not user:
        return False
    if not security.verify_password(password, user.get('password')):
        return False
    return user
