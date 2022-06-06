from fastapi import APIRouter, Depends
from app.core.settings.app import AppSettings
from app.core.config import get_app_settings

from app.api.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository
from fastapi import File, UploadFile
from starlette.responses import StreamingResponse
import io
from PIL import Image
from app.api.acetona.bg import remove
import requests

router = APIRouter()

erode_size = 10

def verify_image(img_content):
    image1 = Image.open(io.BytesIO(img_content))
    return image1.verify()

def convert_image_to_bytes(img):
    image = Image.open(io.BytesIO(img))
    imgio = io.BytesIO()
    image.save(imgio, 'PNG')
    imgio.seek(0)
    return imgio

@router.post("/bg_remover_file", name="bg_remover_file")
async def bg_remover(file:  UploadFile = File(...),
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        contents = await file.read()
        verify_image(contents)
        output = remove(contents, alpha_matting_erode_size=erode_size)
        imgio = convert_image_to_bytes(output)
        return StreamingResponse(content=imgio, media_type="image/png")

    except Exception as e:
        return {"status": str(e)}
        

@router.post("/bg_remover_url", name="bg_remover_url")
async def bg_remover_url(url:  str,
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        contents = requests.get(url).content
        verify_image(contents)
        output = remove(contents, alpha_matting_erode_size=erode_size)
        imgio = convert_image_to_bytes(output)
        return StreamingResponse(content=imgio, media_type="image/png")

    except Exception as e:
        return {"status": str(e)}
        
