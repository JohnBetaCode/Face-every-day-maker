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
import numpy as np
from collections import OrderedDict

# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class Face:
    def __init__(self, shape: list) -> None:
        """!
        Constructor for Face class instances
        @param shape 'np.array' list of landmarks
            detections in face shape
        """

        # Face
        self.shape = shape

        # define a dictionary that maps the indexes of the facial
        # landmarks to specific face regions
        self.FACIAL_LANDMARKS_INDEXES = OrderedDict(
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

    @property
    def mouth(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Mouth"]
        return tuple(self.shape[j:k])

    @property
    def right_eyebrow(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Right_Eyebrow"]
        return tuple(self.shape[j:k])

    @property
    def left_eyebrow(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Left_Eyebrow"]
        return tuple(self.shape[j:k])

    @property
    def right_eye(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Right_Eye"]
        return tuple(self.shape[j:k])

    @property
    def left_eye(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Left_Eye"]
        return tuple(self.shape[j:k])

    @property
    def nose(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Nose"]
        return tuple(self.shape[j:k])

    @property
    def jaw(self) -> tuple:
        (j, k) = self.FACIAL_LANDMARKS_INDEXES["Jaw"]
        return tuple(self.shape[j:k])


class FaceDetector:
    def __init__(self, predictor_path: str) -> None:
        """!
        Constructor for FaceDetector class instances
        @param path 'string' absolute path to the landmarks weights
        """

        self._detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(predictor_path)

        self._graphics_colors = OrderedDict(
            [
                ("Mouth", (19, 199, 109)),
                ("Right_Eyebrow", (79, 76, 240)),
                ("Left_Eyebrow", (230, 159, 23)),
                ("Right_Eye", (168, 100, 168)),
                ("Left_Eye", (158, 163, 32)),
                ("Nose", (163, 38, 32)),
                ("Jaw", (180, 42, 220)),
            ]
        )

    def predict(self, img: np.array) -> Face:
        """!
        Predicts faces in image, but only one is return
        (the last one in being detected)
        @param img 'np.array' image for prediction
        @return _ 'Face' Face class object associated with shape of prediction,
            if not face detected in image None is return
        """

        # detect faces in the grayscale image
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self._detector(img_gray, 1)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = self._predictor(img_gray, rect)
            shape = self.shape_to_numpy_array(shape=shape)

        if not len(rects):
            return None

        return Face(shape=shape)

    def shape_to_numpy_array(self, shape) -> np.array:
        """!
        Converts shape of detections in a numpy array
        @param shape 'list' list of landmarks detections
        @return _ 'np.array' numpy array of landmarks
        """

        # initialize the list of (x, y)-coordinates
        coordinates = np.zeros((68, 2), dtype="int")

        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coordinates[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coordinates

    def visualize_landmarks(
        self,
        img: np.array,
        face: Face,
    ) -> np.array:
        """!
        Draw face detector visuals
        @param img 'np.array' image to draw landmarks and face components
        @param face 'Face' face with landmarks, and components
        @return img 'np.array' image with components drawn
        """

        landmarks = OrderedDict(
            [
                ("Mouth", face.mouth),
                ("Right_Eyebrow", face.right_eyebrow),
                ("Left_Eyebrow", face.left_eyebrow),
                ("Right_Eye", face.right_eye),
                ("Left_Eye", face.left_eye),
                ("Nose", face.nose),
                ("Jaw", face.jaw),
            ]
        )

        for shape_key, shape_values in landmarks.items():
            pts = np.array(shape_values, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], False, self._graphics_colors[shape_key])
            for cnt in shape_values:
                cv2.circle(img, tuple(cnt), 1, (0, 0, 255), -1)

        return img


# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================

# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTION
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================
if __name__ == "__main__":

    face_detector = FaceDetector(
        predictor_path="/workspace/dev_ws/configs/predictor_landmarks.dat"
    )

    # DO NOT DO THIS IN PRODUCTION CODE
    from file_utils import Image

    file_img = Image(
        path="/workspace/dev_ws/media/images/2021_1/IMG_20210104_103925.jpg", load=True
    )

    # get image data from Image File
    img = file_img.get_data(size=(640, 480))

    # predict in image and find faces
    face = face_detector.predict(img=img)

    # show result
    cv2.imshow(
        "face_detector",
        face_detector.visualize_landmarks(img=img, face=face),
    )
    cv2.waitKey(-1)

# =============================================================================
