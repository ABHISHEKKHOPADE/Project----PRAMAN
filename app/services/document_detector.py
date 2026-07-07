import cv2 
import numpy as np
from logger import get_logger

logger = get_logger(__name__)


class DocumentDetector:

    def __init__(self,image_path):
        self.image=cv2.imread(image_path)

        if self.image is None:
            logger.error(f"Image at path {image_path} could not be loaded.")
            raise ValueError(f"Image at path {image_path} could not be loaded")
        

        self.original=self.image.copy()




    #######################################################
    # Detect Aadhaar Document
    #######################################################

    def detect(self):

        gray=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

        blur=cv2.GaussianBlur(gray,(5,5),0)

        edges=cv2.Canny(blur,50,150)

        contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True
        )

        for contour in contours:

            perimeter = cv2.arcLength(
                contour,
                True
            )
            approx = cv2.approxPolyDP(
                contour,
                0.02 * perimeter,
                True
            )

            if len(approx) == 4:

                self.document = approx

                return approx

        return None
    

    #######################################################
    # Draw Rectangle
    #######################################################

    def draw(self):

        if self.detect() is None:

            return self.original

        cv2.drawContours(
            self.original,
            [self.document],
            -1,
            (0, 255, 0),
            3
        )

        return self.original
    


    #######################################################
    # Crop Bounding Box
    #######################################################

    def crop(self):

        if self.detect() is None:

            return None

        x, y, w, h = cv2.boundingRect(
            self.document
        )

        crop = self.image[
            y:y+h,
            x:x+w
        ]

        return crop



        