from app.services.Preprocesser import OCRPreprocessor

processor = OCRPreprocessor(
    r"uploads\download (4).jpeg"
)

image = processor.process()

print("Preprocessing Complete")