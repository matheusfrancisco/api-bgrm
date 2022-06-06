from fastapi import APIRouter

from app.api.routes import users
from app.api.routes import image

router = APIRouter()
router.include_router(users.router, tags=["user"], prefix="/users")
router.include_router(image.router, tags=["image"], prefix="/image")
