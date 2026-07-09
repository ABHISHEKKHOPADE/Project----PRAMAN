from fastapi import APIRouter

from app.database.database import Database

router = APIRouter()


@router.get("/history")

def history():

    db = Database()

    data = db.all()

    db.close()

    result = []

    for row in data:

        result.append({

            "id": row[0],

            "name": row[1],

            "dob": row[2],

            "gender": row[3],

            "aadhaar": row[4],

            "confidence": row[5],

            "similarity": row[6],

            "quality": row[7],

            "tampering": row[8],

            "status": row[9],

            "report": row[10],

            "date": row[11]

        })

    return result