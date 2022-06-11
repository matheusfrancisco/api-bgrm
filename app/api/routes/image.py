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
import sys
import os
from ..miope import blur


router = APIRouter()

erode_size = 0

def convert_bytes_to_image(byts):
    return Image.open(io.BytesIO(byts))

def convert_image_to_bytes(img):
    image = Image.open(io.BytesIO(img))
    imgio = io.BytesIO()
    image.save(imgio, 'PNG')
    imgio.seek(0)
    return imgio

def verify_transparency(img):
    if img.info.get("transparency", None) is not None:
        print('1')
        return True
    elif img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                print('2')
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            print('3')
            return True

    return False

@router.post("/bg_remover_file", name="bg_remover_file")
async def bg_remover(file:  UploadFile = File(...),
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        contents = await file.read()
        img_content = convert_bytes_to_image(contents)

        if verify_transparency(img_content):
            return {"msg": "Tranparency found in this image."}

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
        img_content = convert_bytes_to_image(contents)

        if verify_transparency(img_content):
            return {"msg": "Tranparency found in this image."}

        output = remove(contents, alpha_matting_erode_size=erode_size)
        imgio = convert_image_to_bytes(output)
        return StreamingResponse(content=imgio, media_type="image/png")

    except Exception as e:
        return {"status": str(e)}
        

@router.post("/blur_chars", name="blur_chars")
async def blur_chars(file:  UploadFile = File(...),
                     settings: AppSettings = Depends(get_app_settings),
                     user_repo: UsersRepository = Depends(get_repository(UsersRepository))):
    try:
        contents = await file.read()
        img_content = convert_bytes_to_image(contents)
        resul = blur.identify_text(img_content)
        return StreamingResponse(content=io.BytesIO(resul.tobytes()), media_type="image/png")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return {"status": str(e)}
        