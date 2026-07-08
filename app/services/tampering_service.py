import cv2
import numpy as np
import os


class TamperingService:

    def __init__(self):
        pass

    ####################################################
    ## Read Image
    ####################################################

    def read_image(self, image_path):

        if not os.path.exists(image_path):
            raise FileNotFoundError(image_path)

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Cannot read image.")

        return image

    ####################################################
    ## Noise Analysis
    ####################################################

    def noise_analysis(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        blur = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        noise = cv2.absdiff(
            gray,
            blur
        )

        score = float(
            np.std(noise)
        )

        return round(score, 2)

    ####################################################
    ## Edge Density Analysis
    ####################################################

    def edge_analysis(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        edges = cv2.Canny(
            gray,
            100,
            200
        )

        density = np.sum(edges > 0)

        density /= (
            edges.shape[0] *
            edges.shape[1]
        )

        return round(
            float(density * 100),
            2
        )

    ####################################################
    ## Sharpness / Compression Analysis
    ####################################################

    def compression_analysis(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        laplacian = cv2.Laplacian(
            gray,
            cv2.CV_64F
        )

        score = laplacian.var()

        return round(
            float(score),
            2
        )

    ####################################################
    ## Copy-Move Detection
    ####################################################

    def detect_copy_move(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        orb = cv2.ORB_create(
            2000
        )

        keypoints, descriptors = orb.detectAndCompute(
            gray,
            None
        )

        if descriptors is None:
            return 0

        matcher = cv2.BFMatcher(
            cv2.NORM_HAMMING
        )

        matches = matcher.knnMatch(
            descriptors,
            descriptors,
            k=2
        )

        good_matches = 0

        for pair in matches:

            if len(pair) < 2:
                continue

            m, n = pair

            if (
                m.distance < 0.75 * n.distance
                and abs(m.queryIdx - n.trainIdx) > 20
            ):
                good_matches += 1

        return good_matches

    ####################################################
    ## Metadata Check
    ####################################################

    def metadata_check(self, image_path):

        extension = os.path.splitext(
            image_path
        )[1].lower()

        allowed = [

            ".jpg",

            ".jpeg",

            ".png",

            ".bmp",

            ".webp",

            ".avif"

        ]

        return extension in allowed

    ####################################################
    ## Calculate Risk Score
    ####################################################

    def calculate_risk(

        self,

        noise,

        edge,

        sharpness,

        copy_move,

        metadata

    ):

        risk = 0

        if noise > 18:
            risk += 20

        if edge > 14:
            risk += 20

        if sharpness < 100:
            risk += 20

        if copy_move > 80:
            risk += 30

        if not metadata:
            risk += 10

        return risk

    ####################################################
    ## Complete Analysis
    ####################################################

    def analyze(self, image_path):

        image = self.read_image(
            image_path
        )

        noise = self.noise_analysis(
            image
        )

        edge = self.edge_analysis(
            image
        )

        sharpness = self.compression_analysis(
            image
        )

        copy_move = self.detect_copy_move(
            image
        )

        metadata = self.metadata_check(
            image_path
        )

        risk = self.calculate_risk(

            noise,

            edge,

            sharpness,

            copy_move,

            metadata

        )

        report = {

            "status": "PASS"
            if risk < 50
            else "FAIL",

            "risk_score": risk,

            "tampered": risk >= 50,

            "checks": {

                "noise_score": noise,

                "edge_density": edge,

                "sharpness": sharpness,

                "copy_move_matches": copy_move,

                "metadata_valid": metadata

            }

        }

        return report