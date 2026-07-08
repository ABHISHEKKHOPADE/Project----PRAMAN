import os
import cv2
import numpy as np
from PIL import Image
import pillow_avif
from sklearn.metrics.pairwise import cosine_similarity
from insightface.app import FaceAnalysis


class FaceVerificationService:

    def __init__(self):

        print("Loading Face Model...")

        self.app = FaceAnalysis(name="buffalo_l")

        self.app.prepare(
            ctx_id=0 if cv2.cuda.getCudaEnabledDeviceCount() > 0 else -1,
            det_size=(640, 640)
        )

        print("Face Model Loaded")

    ####################################################
    # Universal Image Loader
    ####################################################

    def read_image(self, image_path):

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        ext = os.path.splitext(image_path)[1].lower()

        # AVIF Support
        if ext == ".avif":

            image = Image.open(image_path).convert("RGB")
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            return image

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")

        return image

    ####################################################
    # Detect Face
    ####################################################

    def detect_face(self, image_path):

        image = self.read_image(image_path)

        faces = self.app.get(image)

        if len(faces) == 0:
            return None

        # Largest face
        largest = max(
            faces,
            key=lambda face: (
                (face.bbox[2] - face.bbox[0]) *
                (face.bbox[3] - face.bbox[1])
            )
        )

        return largest

    ####################################################
    # Face Embedding
    ####################################################

    def get_embedding(self, image_path):

        face = self.detect_face(image_path)

        if face is None:
            return None

        return face.embedding

    ####################################################
    # Face Verification
    ####################################################

    def verify(self, aadhaar_image, selfie_image):

        emb1 = self.get_embedding(aadhaar_image)
        emb2 = self.get_embedding(selfie_image)

        if emb1 is None:
            return {
                "status": "FAIL",
                "message": "No face found in Aadhaar image"
            }

        if emb2 is None:
            return {
                "status": "FAIL",
                "message": "No face found in Selfie"
            }

        similarity = cosine_similarity(
            emb1.reshape(1, -1),
            emb2.reshape(1, -1)
        )[0][0]

        similarity_percent = round(float(similarity * 100), 2)

        return {

            "status": "PASS",

            "aadhaar_face": True,

            "selfie_face": True,

            "similarity": similarity_percent,

            "verified": similarity_percent >= 60

        }

    ####################################################
    # Draw Face Bounding Box
    ####################################################

    def draw_face(
        self,
        image_path,
        output_path="processed/face_detected.jpg"
    ):

        image = self.read_image(image_path)

        face = self.detect_face(image_path)

        if face is None:
            return None

        x1, y1, x2, y2 = face.bbox.astype(int)

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            3
        )

        cv2.putText(
            image,
            "Face",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cv2.imwrite(output_path, image)

        return output_path