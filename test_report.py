import json

from app.services.report_service import ReportService

quality = {
    "status": "PASS",
    "blur_score": 252.6,
    "resolution": "1200x800"
}

ocr = {
    "status": "PASS",
    "total_lines": 10
}

parser = {
    "status": "PASS",
    "name": "Sutapa Pal Datta",
    "dob": "26/01/1979",
    "gender": "Female",
    "aadhaar_number": "6641 2804 9316"
}

face = {
    "status": "PASS",
    "verified": True,
    "similarity": 91.5
}

tampering = {
    "status": "PASS",
    "tampered": False,
    "risk_score": 18
}

service = ReportService()

report = service.generate(
    quality,
    ocr,
    parser,
    face,
    tampering
)

print(json.dumps(report, indent=4))

path = service.save(report)

print("\nSaved to:", path)