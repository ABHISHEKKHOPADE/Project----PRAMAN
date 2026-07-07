import cv2
import os
from logger import get_logger

logger = get_logger(__name__)


class ImageEnhancer:
    def __init__(self,image_path):
        self.image_path=image_path

        self.image=cv2.imread(image_path)

        if self.image is None:
            logger.error(f"Image at path {image_path} could not be loaded.")
            raise ValueError(f"Image at path {image_path} could not be loaded")
        

    ##################################################
    # Denoising
    ##################################################

    def denoise(self):
        self.image=cv2.fastNlMeansDenoisingColored(self.image,None,10,10,7,21)

        return self
    

    ##################################################
    # Clahe Contrast Enhancement
    ##################################################

    def enhance_contrast(self):
        lab=cv2.cvtColor(self.image,cv2.COLOR_BGR2LAB)

        l,a,b=cv2.split(lab)

        clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))

        l=clahe.apply(l)

        lab=cv2.merge((l,a,b))

        self.image=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)

        return self
    
    ##################################################
    # Sharpen
    ##################################################

    def sharpen(self):

        kernel = [
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ]

        import numpy as np

        kernel = np.array(kernel)

        self.image = cv2.filter2D(
            self.image,
            -1,
            kernel
        )

        return self
    

    ##################################################
    # Resize
    ##################################################

    def resize(self,scale=1.5):
        h,w=self.image.shape[:2]

        self.image=cv2.resize(self.image,(int(w*scale),int(h*scale)))


        return self
    

    ##################################################
    # Save
    ##################################################

    def save(self,output_path):
        folder = os.path.dirname(output_path)

        os.makedirs(folder, exist_ok=True)

        cv2.imwrite(output_path, self.image)

        return output_path
    

    






    