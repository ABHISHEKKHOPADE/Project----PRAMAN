from fastapi import FastAPI

from app.routes.verify import router as verify_router
from app.routes.ocr import router as ocr_router
from app.routes.face import router as face_router
from app.routes.quality import router as quality_router
from app.routes.tampering import router as tampering_router

app = FastAPI(

    title="PRAMAN API",

    version="1.0.0",

    description="Aadhaar Verification System"

)
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "PRAMAN API is running "
    }

app.include_router(
    verify_router
)

app.include_router(
    ocr_router
)

app.include_router(
    face_router
)

app.include_router(
    quality_router
)

app.include_router(
    tampering_router
)