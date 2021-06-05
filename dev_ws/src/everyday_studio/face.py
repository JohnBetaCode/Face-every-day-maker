# =============================================================================
"""
Author: John Betacourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================

import cv2
import dlib
import imutils
import numpy as np
from collections import OrderedDict

# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class Face:
    def __init__(self):
        pass


class FaceDetector:
    def __init__(self, predictor_path: str) -> None:

        self._detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(predictor_path)

        self._facial_features_cordinates = {}

        # define a dictionary that maps the indexes of the facial
        # landmarks to specific face regions
        self._FACIAL_LANDMARKS_INDEXES = OrderedDict(
            [
                ("Mouth", (48, 68)),
                ("Right_Eyebrow", (17, 22)),
                ("Left_Eyebrow", (22, 27)),
                ("Right_Eye", (36, 42)),
                ("Left_Eye", (42, 48)),
                ("Nose", (27, 35)),
                ("Jaw", (0, 17)),
            ]
        )

    def predict(self, img: np.array):

        img = imutils.resize(img, width=500)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image

        rects = self._detector(img_gray, 1)

        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = self._predictor(img_gray, rect)
            shape = self.shape_to_numpy_array(shape=shape)

            output = self.visualize_facial_landmarks(img, shape)
            cv2.imshow("Image", output)
            cv2.waitKey(0)

    def shape_to_numpy_array(self, shape, dtype="int"):

        # initialize the list of (x, y)-coordinates
        coordinates = np.zeros((68, 2), dtype=dtype)

        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coordinates[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coordinates

    def visualize_facial_landmarks(self, image, shape, colors=None, alpha=0.75):

        # create two copies of the input image -- one for the
        # overlay and one for the final output image
        overlay = image.copy()
        output = image.copy()

        # if the colors list is None, initialize it with a unique
        # color for each facial landmark region
        if colors is None:
            colors = [
                (19, 199, 109),
                (79, 76, 240),
                (230, 159, 23),
                (168, 100, 168),
                (158, 163, 32),
                (163, 38, 32),
                (180, 42, 220),
            ]

        # loop over the facial landmark regions individually
        for (i, name) in enumerate(self._FACIAL_LANDMARKS_INDEXES.keys()):
            # grab the (x, y)-coordinates associated with the
            # face landmark
            (j, k) = self._FACIAL_LANDMARKS_INDEXES[name]
            pts = shape[j:k]
            self._facial_features_cordinates[name] = pts

            # check if are supposed to draw the jawline
            if name == "Jaw":
                # since the jawline is a non-enclosed facial region,
                # just draw lines between the (x, y)-coordinates
                for l in range(1, len(pts)):
                    ptA = tuple(pts[l - 1])
                    ptB = tuple(pts[l])
                    cv2.line(overlay, ptA, ptB, colors[i], 2)

            # otherwise, compute the convex hull of the facial
            # landmark coordinates points and display it
            else:
                hull = cv2.convexHull(pts)
                cv2.drawContours(overlay, [hull], -1, colors[i], -1)

        # apply the transparent overlay
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

        return output


# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================

# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTION
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================
if __name__ == "__main__":

    face_detector = FaceDetector(
        predictor_path="/workspace/dev_ws/configs/shape_predictor_68_face_landmarks.dat"
    )

    from file_utils import Image

    file_img = Image(
        path="/workspace/dev_ws/media/images/2021_1/IMG_20210104_103925.jpg", load=True
    )

    face_detector.predict(img=file_img.image)

# =============================================================================
