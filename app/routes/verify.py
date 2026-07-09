from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os
import shutil

from app.services.Image_quality import ImageQualityAnalyzer
from app.services.ocr_service import OCRService
from app.services.aadhaar_parser import AadhaarParser
from app.services.face_service import FaceVerificationService
from app.services.tampering_service import TamperingService

from app.utils.pdf_report import PDFReportGenerator
from app.database.database import Database

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/verify")
async def verify(

    aadhaar: UploadFile = File(...),

    selfie: UploadFile = File(...)

):

    aadhaar_path = os.path.join(
        UPLOAD_DIR,
        aadhaar.filename
    )

    selfie_path = os.path.join(
        UPLOAD_DIR,
        selfie.filename
    )

    with open(
        aadhaar_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            aadhaar.file,
            buffer
        )

    with open(
        selfie_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            selfie.file,
            buffer
        )

    #####################################################
    # Image Quality
    #####################################################

    #####################################################
# Image Quality
#####################################################

    quality = ImageQualityAnalyzer(aadhaar_path)

    quality_report = quality.analyze()

    #####################################################
    # OCR
    #####################################################

    ocr = OCRService()

    ocr_report = ocr.extract_text(
        aadhaar_path
    )

    #####################################################
    # Aadhaar Parsing
    #####################################################

    parser = AadhaarParser(
        ocr_report
    )

    aadhaar_data = parser.parse()

    #####################################################
    # Face Verification
    #####################################################

    face = FaceVerificationService()

    face_report = face.verify(

        aadhaar_path,

        selfie_path

    )

    #####################################################
    # Tampering
    #####################################################

    tampering = TamperingService()

    tamper_report = tampering.analyze(
        aadhaar_path
    )

        #####################################################
    # Confidence
    #####################################################

    confidence = 100

    if quality_report["status"] == "FAIL":
        confidence -= 20

    if not face_report["verified"]:
        confidence -= 30

    if tamper_report["tampered"]:
        confidence -= 20

    if aadhaar_data["aadhaar_number"] is None:
        confidence -= 15

    if aadhaar_data["name"] is None:
        confidence -= 15

    confidence = max(confidence, 0)

    status = "PASS" if confidence > 60 else "FAIL"

    #####################################################
    # Final Report
    #####################################################

    final_report = {

        "status": status,

        "confidence": confidence,

        "image_quality": quality_report,

        "ocr": ocr_report,

        "aadhaar": aadhaar_data,

        "face": face_report,

        "tampering": tamper_report

    }

    #####################################################
    # Generate PDF
    #####################################################

    pdf = PDFReportGenerator()

    pdf_path = pdf.generate(final_report)

    final_report["pdf_report"] = pdf_path
    db = Database()

    db.insert(final_report)

    db.close()

    #####################################################
    # Return
    #####################################################

    return final_report