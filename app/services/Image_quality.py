import os
import cv2
import numpy as np
from PIL import Image
import pillow_avif
from logger import get_logger

logger = get_logger(__name__)


class ImageQualityAnalyzer:

    def __init__(self, image_path):

        self.image_path = image_path

        if not os.path.exists(image_path):
            raise FileNotFoundError(image_path)

        ext = os.path.splitext(image_path)[1].lower()

        # AVIF Support
        if ext == ".avif":

            image = Image.open(image_path).convert("RGB")
            image = np.array(image)
            self.image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        else:

            self.image = cv2.imread(image_path)

        if self.image is None:
            raise ValueError(
                f"Image at path {image_path} could not be loaded."
            )

        self.gray = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

    ####################################################
    # Blur
    ####################################################

    def blur_score(self):

        score = cv2.Laplacian(
            self.gray,
            cv2.CV_64F
        ).var()

        logger.info(f"Blur Score : {score}")

        return float(score)

    def is_blurry(self, threshold=100):

        return self.blur_score() < threshold

    ####################################################
    # Brightness
    ####################################################

    def brightness(self):

        value = np.mean(self.gray)

        logger.info(f"Brightness : {value}")

        return float(value)

    def brightness_status(self):

        b = self.brightness()

        if b < 60:
            return "dark"

        elif b > 200:
            return "bright"

        return "normal"

    ####################################################
    # Contrast
    ####################################################

    def contrast(self):

        value = self.gray.std()

        logger.info(f"Contrast : {value}")

        return float(value)

    ####################################################
    # Resolution
    ####################################################

    def resolution(self):

        h, w = self.image.shape[:2]

        return int(w), int(h)

    ####################################################
    # Noise
    ####################################################

    def noise(self):

        gray = self.gray.astype(np.float32)

        blur = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        score = np.mean(
            np.abs(gray - blur)
        )

        logger.info(f"Noise : {score}")

        return float(score)

    ####################################################
    # Glare
    ####################################################

    def glare_score(self):

        bright = np.sum(self.gray > 240)

        total = self.gray.size

        glare = (bright / total) * 100

        logger.info(f"Glare : {glare}")

        return float(glare)

    ####################################################
    # Final Analysis
    ####################################################

    def analyze(self):

        issues = []

        blur = self.blur_score()

        brightness = self.brightness()

        contrast = self.contrast()

        width, height = self.resolution()

        noise = self.noise()

        glare = self.glare_score()

        if blur < 120:
            issues.append("Image is blurry")

        if brightness < 60:
            issues.append("Image is too dark")

        elif brightness > 240:
            issues.append("Image is too bright")

        if width < 640 or height < 480:
            issues.append("Low Resolution")

        if glare > 70:
            issues.append("Too much glare")

        if noise > 20:
            issues.append("High noise")

        return {

            "status": "PASS" if len(issues) == 0 else "FAIL",

            "issues": issues,

            "metrics": {

                "blur_score": float(round(blur, 2)),

                "brightness": float(round(brightness, 2)),

                "contrast": float(round(contrast, 2)),

                "resolution": {

                    "width": int(width),

                    "height": int(height)

                },

                "noise_score": float(round(noise, 2)),

                "glare_percentage": float(round(glare, 2))

            }

        }