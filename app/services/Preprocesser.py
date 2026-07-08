from PIL import Image
import pillow_avif
import cv2
import numpy as np
import os
from app.Configuration.config import Config


class OCRPreprocessor:

    def __init__(self, image_path):

        img = Image.open(image_path)

        self.image = cv2.cvtColor(
            np.array(img),
            cv2.COLOR_RGB2BGR
        )

        if self.image is None:
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

    ###################################################
    # Resize
    ###################################################

    def resize(self):

        self.image = cv2.resize(
            self.image,
            None,
            fx=Config.RESIZE_SCALE,
            fy=Config.RESIZE_SCALE,
            interpolation=cv2.INTER_CUBIC
        )

        return self

    ###################################################
    # Grayscale
    ###################################################

    def grayscale(self):

        self.image = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

        return self

    ###################################################
    # CLAHE
    ###################################################

    def clahe(self):

        clahe = cv2.createCLAHE(
            clipLimit=Config.CLAHE_CLIP_LIMIT,
            tileGridSize=Config.CLAHE_GRID_SIZE
        )

        self.image = clahe.apply(self.image)

        return self

    ###################################################
    # Denoise
    ###################################################

    def denoise(self):

        self.image = cv2.fastNlMeansDenoising(
            self.image,
            None,
            15,
            7,
            21
        )

        return self

    ###################################################
    # Gaussian Blur
    ###################################################

    def gaussian(self):

        self.image = cv2.GaussianBlur(
            self.image,
            Config.GAUSSIAN_KERNEL,
            0
        )

        return self

    ###################################################
    # Adaptive Threshold
    ###################################################

    def threshold(self):

        self.image = cv2.adaptiveThreshold(

            self.image,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY,

            Config.BLOCK_SIZE,

            Config.C

        )

        return self

    ###################################################
    # Morphology
    ###################################################

    def morphology(self):

        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (2, 2)
        )

        self.image = cv2.morphologyEx(
            self.image,
            cv2.MORPH_CLOSE,
            kernel
        )

        return self

    ###################################################
    # Save
    ###################################################

    def save(self, name):

        os.makedirs(
            "processed",
            exist_ok=True
        )

        path = os.path.join(
            "processed",
            name
        )

        cv2.imwrite(
            path,
            self.image
        )

    ###################################################
    # Complete Pipeline
    ###################################################

    def process(self):

        (
            self.resize()
                .grayscale()
                .clahe()
                .denoise()
                .gaussian()
                .threshold()
                .morphology()
        )

        if Config.SAVE_DEBUG_IMAGES:

            self.save(
                "preprocessed.jpg"
            )

        return self.image