from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import shutil
import os

from app.services.ocr_service import OCRService

router = APIRouter(

    prefix="/ocr",

    tags=["OCR"]

)

UPLOAD_FOLDER = "uploads"

@router.post("/")
async def ocr(

    image: UploadFile = File(...)

):

    path = os.path.join(

        UPLOAD_FOLDER,

        image.filename

    )

    with open(path, "wb") as buffer:

        shutil.copyfileobj(
            image.file,
            buffer
        )

    return OCRService().extract_text(path)