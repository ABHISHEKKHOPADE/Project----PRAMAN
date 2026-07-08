import json

from app.services.ocr_service import OCRService


ocr = OCRService()

report = ocr.extract_text(
    r"E:\pr1\Project----PRAMAN\uploads\dholewal-aadhaar-card-center-dholewal-ludhiana-aadhaar-card-agents-7mb380p7h3.avif",
)

print("\nOCR REPORT\n")

print(
    json.dumps(
        report,
        indent=4
    )
)

output = ocr.draw_boxes(
    r"uploads\download (4).jpeg",
    report
)

print("\nAnnotated Image Saved At:")

print(output)