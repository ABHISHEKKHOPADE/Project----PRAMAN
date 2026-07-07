from app.services.Image_enhancement import ImageEnhancer

# enhancer = ImageEnhancer("uploads/aadhaar.jpg")
enhancer=ImageEnhancer(r"uploads\download (4).jpeg")


enhancer\
    .denoise() \
    .enhance_contrast() \
    .sharpen() \
    .resize(1.3) \
    .save("processed/enhanced_aadhaar.jpg")

print("Image enhancement completed.")