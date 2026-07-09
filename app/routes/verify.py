from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import shutil
import os

from app.services.Image_quality import ImageQualityAnalyzer
from app.services.ocr_service import OCRService
from app.services.aadhaar_parser import AadhaarParser
from app.services.face_service import FaceVerificationService
from app.services.tampering_service import TamperingService
from app.services.report_service import ReportService

router = APIRouter(

    prefix="/verify",

    tags=["Complete Verification"]

)

UPLOAD = "uploads"

os.makedirs(
    UPLOAD,
    exist_ok=True
)


@router.post("/")
async def verify(

    aadhaar: UploadFile = File(...),

    selfie: UploadFile = File(...)

):

    aadhaar_path = os.path.join(
        UPLOAD,
        aadhaar.filename
    )

    selfie_path = os.path.join(
        UPLOAD,
        selfie.filename
    )

    with open(aadhaar_path, "wb") as f:
        shutil.copyfileobj(
            aadhaar.file,
            f
        )

    with open(selfie_path, "wb") as f:
        shutil.copyfileobj(
            selfie.file,
            f
        )

    quality = ImageQualityAnalyzer().analyze(
        aadhaar_path
    )

    ocr = OCRService().extract_text(
        aadhaar_path
    )

    parser = AadhaarParser(
        ocr
    ).parse()

    face = FaceVerificationService().verify(

        aadhaar_path,

        selfie_path

    )

    tampering = TamperingService().analyze(
        aadhaar_path
    )

    report = ReportService().generate(

        quality,

        ocr,

        parser,

        face,

        tampering

    )

    ReportService().save(report)

    return report