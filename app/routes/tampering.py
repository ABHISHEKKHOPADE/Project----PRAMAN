from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import shutil
import os

from app.services.tampering_service import TamperingService

router = APIRouter(

    prefix="/tampering",

    tags=["Tampering"]

)

UPLOAD_FOLDER = "uploads"

@router.post("/")
async def tampering(

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

    return TamperingService().analyze(path)