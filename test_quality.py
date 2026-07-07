from app.services.Image_quality import ImageQualityAnalyzer


image=ImageQualityAnalyzer("uploads\download (4).jpeg")

report=image.analyze_image_quality()


print("\nImage Quality Report")


for key,value in report.items():
    print(f"{key:<20}:{value}")