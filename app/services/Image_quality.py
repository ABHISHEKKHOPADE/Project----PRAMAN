import cv2
import numpy as np
from logger import get_logger

logger = get_logger(__name__)

class ImageQualityAnalyzer:
    def __init__(self,image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            logger.error(f"Image at path {image_path} could not be loaded.")
            raise ValueError(f"Image at path {image_path} could not be loaded.")
        self.gray=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

    ####################################################
    # Blurriness Detection
    ####################################################

    
    def blur_score(self):

        laplician_var=cv2.Laplacian((self.gray),cv2.CV_64F).var()
        logger.info(f"Blur score (Laplacian variance) for image {self.image_path}: {laplician_var}")
        return laplician_var
    
    def is_blurry(self,threshold=100.00):
        score=self.blur_score()
        is_blurry=score<threshold
        logger.info(f"Image {self.image_path} is {'blurry' if is_blurry else 'not blurry'} with a score of {score} and threshold of {threshold}.")
        return is_blurry

    ####################################################
    # Brightness
    ####################################################


    def brightness(self):

        mean= np.mean(self.gray)
        
        logger.info(f"Brightness analysis for image {self.image_path}: mean={mean}")
        return mean

    def brightness_status(self,threshold_low1=60,threshold_high=200):
        mean=self.brightness()
        if mean<threshold_low1:
            status="dark"
        elif mean>threshold_high:
            status="bright"
        else:
            status="normal"

        logger.info(f"Brightness status for image {self.image_path}: {status}")
        return status
    


    ####################################################
    # Contrast
    ####################################################

    def contrast(self):
        contrast_score=self.gray.std()
        logger.info(f"Contrast analysis for image {self.image_path}: contrast={contrast_score}")  
        return contrast_score
    
    ####################################################
    # Resolution
    ####################################################

    def resolution(self):
        height,width=self.image.shape[:2]
        logger.info(f"Resolution analysis for image {self.image_path}: width={width}, height={height}")
        return width,height
    

    ####################################################
    # Noise
    ####################################################


    def Noise(self):
        gray=self.gray.astype(np.float32)
        blurr=cv2.GaussianBlur(gray,(3,3),0).astype(np.float32)

        noise=np.mean(np.abs(gray-blurr))

        logger.info(f"Noise analysis for image {self.image_path}: noise={noise}")
        return noise
    



    ####################################################
    # Glare Detection
    ####################################################

    def glare_score(self):
        bright_pixels=np.sum(self.gray>240)
        total_pixels=self.gray.size

        glare_ratio=round(bright_pixels/total_pixels,2)
        logger.info(f"Glare analysis for image {self.image_path}: glare_ratio={glare_ratio}")
        return glare_ratio*100
    



    ####################################################
    # Complete Analysis
    ####################################################

    def analyze(self):

        issues = []

        # Blur
        blur = self.blur_score()
        if blur < 120:
            issues.append("Image is blurry")

        # Brightness
        brightness = self.brightness()
        if brightness < 60:
            issues.append("Image is too dark")
        elif brightness > 240:
            issues.append("Image is too bright")

        # Resolution
        width, height = self.resolution()
        if width < 64 or height < 64:
            issues.append("Low resolution")

        # Glare
        glare = self.glare_score()
        if glare > 70:
            issues.append("Too much glare")

        # Noise
        noise = self.Noise()
        if noise > 20:
            issues.append("Image contains excessive noise")

        result = {
            "status": "PASS" if len(issues) == 0 else "FAIL",
            "issues": issues,
            "metrics": {
                "blur_score": round(blur, 2),
                "brightness": round(brightness, 2),
                "contrast": round(self.contrast(), 2),
                "resolution": {
                    "width": width,
                    "height": height
                },
                "noise_score": round(noise, 2),
                "glare_percentage": glare
            }
        }

        return result



