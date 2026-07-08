import json

from app.services.ocr_service import OCRService
from app.services.aadhaar_parser import AadhaarParser

IMAGE = r"uploads\images (3).jpeg"

ocr = OCRService()

ocr_report = ocr.extract_text(IMAGE)

parser = AadhaarParser(ocr_report)

parser.print_ocr()

print("\nFULL TEXT\n")
print(parser.full_text)

result = parser.parse()

print(json.dumps(result, indent=4))