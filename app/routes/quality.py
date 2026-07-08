from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File


import shutil
import os

from app.services.Image_quality import ImageQualityAnalyzer

router=APIRouter(prefix="/quality",tags=["Image Quality"])

UPLOAD_FOLDER="uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)


@router.post("/")

async def quality(
    image:UploadFile=File(...)
):
    
    path=os.path.json(
        UPLOAD_FOLDER,image.filename
    )

    with open(path,"wb") as buff:
        shutil.copyfileobj(image.file,
                           buff)
        


    report = ImageQualityAnalyzer.analyze(path)
    

    return report  