import cv2
import easyocr
import numpy as np
from app.services.Preprocesser import OCRPreprocessor


class OCRService:

    def __init__(self):

        print("Loading EasyOCR Model...")

        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

        print("OCR Model Loaded")

    ##########################################################
    # Extract Text
    ##########################################################

    def extract_text(self, image_path):

        processed = OCRPreprocessor(image_path).process()

        detections = self.reader.readtext(
            processed,
            detail=1,
            paragraph=False,
            decoder="beamsearch",
            width_ths=0.7,
            height_ths=0.7,
            text_threshold=0.4,
            low_text=0.25,
            link_threshold=0.4
        )

        results = []

        for detection in detections:

            try:
                bbox, text, confidence = detection
            except ValueError:
                continue

            confidence = float(confidence)

            # Ignore low confidence detections
            if confidence < 0.30:
                continue

            text = text.strip()

            # Ignore empty text
            if len(text) < 2:
                continue

            # Ignore only punctuation
            if text in ["{", "}", "~", "|", ".", ",", ";", ":"]:
                continue

            pts = []

            for p in bbox:
                pts.append(
                    [
                        int(p[0]),
                        int(p[1])
                    ]
                )

            results.append({

                "text": text,

                "confidence": round(confidence, 3),

                "bbox": pts

            })

        return {

            "status": "PASS" if len(results) else "FAIL",

            "total_lines": len(results),

            "results": results

        }

    ##########################################################
    # Draw OCR Boxes
    ##########################################################

    def draw_boxes(

            self,

            image_path,

            report,

            output_path="processed/ocr_output.jpg"

    ):

        image = cv2.imread(image_path)

        if image is None:

            raise FileNotFoundError(image_path)

        image = cv2.resize(

            image,

            None,

            fx=3,

            fy=3,

            interpolation=cv2.INTER_CUBIC

        )

        for item in report["results"]:

            pts = np.array(

                item["bbox"],

                dtype=np.int32

            )

            cv2.polylines(

                image,

                [pts],

                True,

                (0, 255, 0),

                2

            )

            x = pts[0][0]

            y = pts[0][1]

            cv2.putText(

                image,

                item["text"],

                (x, y - 5),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0, 0, 255),

                2

            )

        cv2.imwrite(

            output_path,

            image

        )

        return output_path