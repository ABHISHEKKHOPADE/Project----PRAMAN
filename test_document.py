import cv2

from app.services.document_detector import DocumentDetector

detector = DocumentDetector(
    r"E:\pr1\Project----PRAMAN\uploads\images (2).jpeg")

outlined = detector.draw()

cv2.imwrite(
    "processed/document_detected.jpg",
    outlined
)

crop = detector.crop()

if crop is not None:

    cv2.imwrite(
        "processed/cropped.jpg",
        crop
    )

print("Document Detection Completed")