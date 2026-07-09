from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import shutil
import os

from app.services.face_service import FaceVerificationService

router = APIRouter(

    prefix="/face",

    tags=["Face Verification"]

)

UPLOAD_FOLDER = "uploads"

@router.post("/")
async def verify_face(

    aadhaar: UploadFile = File(...),

    selfie: UploadFile = File(...)

):

    aadhaar_path = os.path.join(

        UPLOAD_FOLDER,

        aadhaar.filename

    )

    selfie_path = os.path.join(

        UPLOAD_FOLDER,

        selfie.filename

    )

    with open(aadhaar_path, "wb") as buffer:

        shutil.copyfileobj(
            aadhaar.file,
            buffer
        )

    with open(selfie_path, "wb") as buffer:

        shutil.copyfileobj(
            selfie.file,
            buffer
        )

    return FaceVerificationService().verify(

        aadhaar_path,

        selfie_path

    )