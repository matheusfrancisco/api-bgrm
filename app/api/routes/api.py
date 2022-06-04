from fastapi import APIRouter

from app.api.routes import users
from app.api.routes import bg_remover

router = APIRouter()
router.include_router(users.router, tags=["user"], prefix="/users")
router.include_router(bg_remover.router, tags=["bg_remover"], prefix="/bg_remover")
