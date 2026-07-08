import json
import os
from datetime import datetime


class ReportService:

    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    ####################################################
    ## Generate Report
    ####################################################

    def generate(

        self,

        quality_report,

        ocr_report,

        parser_report,

        face_report,

        tampering_report

    ):

        confidence = 100

        if quality_report["status"] == "FAIL":
            confidence -= 20

        if face_report["status"] == "FAIL":
            confidence -= 30

        if tampering_report["tampered"]:
            confidence -= 40

        if parser_report["aadhaar_number"] is None:
            confidence -= 20

        confidence = max(0, confidence)

        final_status = (

            "VERIFIED"

            if confidence >= 70

            else "REJECTED"

        )

        report = {

            "status": final_status,

            "confidence": confidence,

            "generated_at": str(
                datetime.now()
            ),

            "image_quality": quality_report,

            "ocr": {

                "status": ocr_report["status"],

                "total_lines": ocr_report["total_lines"]

            },

            "aadhaar": parser_report,

            "face": face_report,

            "tampering": tampering_report

        }

        return report

    ####################################################
    ## Save JSON
    ####################################################

    def save(

        self,

        report,

        filename="verification_report.json"

    ):

        path = os.path.join(

            "reports",

            filename

        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                report,

                f,

                indent=4

            )

        return path