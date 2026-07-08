import json

from app.services.tampering_service import TamperingService

IMAGE = r"uploads\images (3).jpeg"

service = TamperingService()

report = service.analyze(IMAGE)

print(json.dumps(report, indent=4))