from app.services.Image_quality import ImageQualityAnalyzer

import json

image=ImageQualityAnalyzer("uploads\download (4).jpeg")

report=image.analyze()


print(report)


