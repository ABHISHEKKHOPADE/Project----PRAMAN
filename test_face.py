import json
from app.services.face_service import FaceVerificationService

service = FaceVerificationService()

AADHAAR = r"uploads\Adhar.avif"
SELFIE = r"uploads\selfie2.png"

result = service.verify(AADHAAR, SELFIE)

print(json.dumps(result, indent=4))

output = service.draw_face(AADHAAR)

print("Output saved:", output)