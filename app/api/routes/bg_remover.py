from fastapi import APIRouter, Depends
from app.core.settings.app import AppSettings
from app.core.config import get_app_settings

from app.api.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository
from fastapi import File, UploadFile
from starlette.responses import StreamingResponse
import io
from PIL import Image
from app.aguamicelar.app import remove

router = APIRouter()

@router.post("/", name="bg_remover")
async def bg_remover(file:  UploadFile = File(...),
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        contents = await file.read()
        output = remove(contents)
        image = Image.open(io.BytesIO(output))
        imgio = io.BytesIO()
        image.save(imgio, 'PNG')
        imgio.seek(0)
        return StreamingResponse(content=imgio, media_type="image/png")

    except Exception as e:
        return {"status": str(e)}