import json

from app.services.ocr_service import OCRService


ocr = OCRService()

report = ocr.extract_text(
    r"uploads\aadhaar.jpg"
)

print("\nOCR REPORT\n")

print(
    json.dumps(
        report,
        indent=4
    )
)

output = ocr.draw_boxes(
    r"uploads\aadhaar.jpg",
    report
)

print("\nAnnotated Image Saved At:")

print(output)