import cv2
import easyocr
import numpy as np
from app.services.Preprocesser import OCRPreprocessor


class OCRService:

    def __init__(self):
        print("Loading EasyOCR Model...")

        self.reader = easyocr.Reader(
            ['en','hi'],
            gpu=False
        )
        print("OCR Model Loaded")

    ##########################################################
    # Extract Text
    ##########################################################

    def extract_text(self, image_path):

        processed = OCRPreprocessor(
            image_path
        ).process()

        detections = self.reader.readtext(
            processed,
            detail=1,
            paragraph=False
        )

        # annotated = cv2.cvtColor(
        #     processed,
        #     cv2.COLOR_GRAY2BGR
        # )

        results = []

        for detection in detections:

            bbox, text, confidence = detection

            confidence = float(confidence)

            pts = []

            for p in bbox:

                pts.append(
                    (int(p[0]), 
                     int(p[1])
                     )
                )

            # cv2.polylines(
            #     annotated,
            #     [cv2.convexHull(
            #         cv2.UMat(
            #             cv2.convexHull
            #         )
            #     )],
            #     True,
            #     (0, 255, 0),
            #     2
            # )

            # x = pts[0][0]
            # y = pts[0][1]

            # cv2.putText(
            #     annotated,
            #     text,
            #     (x, y - 5),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.5,
            #     (0, 0, 255),
            #     1
            # )

            results.append({

                "text": text,

                "confidence": round(
                    confidence,
                    3
                ),

                "bounding_box": pts

            })

        return {

            "status":
                "PASS"
                if len(results)
                else "FAIL",

            "total_lines":
                len(results),

            "results":
                results,

            # "image":
            #     annotated

        }
    
     ##########################################################
    # Draw Bounding Boxes
    ##########################################################

    def draw_boxes(
            self,
            image_path,
            report,
            output_path="processed/ocr_output.jpg"
    ):

        image = cv2.imread(image_path)

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

                (0,255,0),

                2

            )

            x = pts[0][0]

            y = pts[0][1]

            cv2.putText(

                image,

                item["text"],

                (x,y-5),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0,0,255),

                2

            )

        cv2.imwrite(
            output_path,
            image
        )

        return output_path