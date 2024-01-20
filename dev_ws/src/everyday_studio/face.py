# =============================================================================
"""
Author: John Betacourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================
import sys

sys.path.append("/workspace/dev_ws/src/background_removal")

import os
from selfieSegmentation import MPSegmentation
from faceDetection import MPFaceDetection
from engine import Engine
import cv2
import copy


# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class FaceStudio:
    def __init__(self) -> None:
        self._FACE_STUDIO_BLURRING_THRESH = float(
            os.getenv("FACE_STUDIO_BLURRING_THRESH", default=0.5)
        )
        self._FACE_STUDIO_BLURRING_RATIO = int(
            os.getenv("FACE_STUDIO_BLURRING_RATIO", default=45)
        )
        self._FACE_STUDIO_BLURRING = int(os.getenv("FACE_STUDIO_BLURRING", default=1))
        self._FACE_STUDIO_GRAY = int(os.getenv("FACE_STUDIO_GRAY", default=1))

        self.FaceSegmentation = Engine(
            show=False, 
            custom_objects=[
                MPSegmentation(
                    threshold=self._FACE_STUDIO_BLURRING_THRESH,
                    bg_images_path="",
                    bg_blur_ratio=(
                        self._FACE_STUDIO_BLURRING_RATIO,
                        self._FACE_STUDIO_BLURRING_RATIO,
                    ),
                ), 
                MPFaceDetection() , 
            ]
        )

    def process(self, frame):

        frame_results = self.FaceSegmentation.custom_processing(frame=copy.copy(frame))
        
        cv2.imshow("debug", self.draw_face_detection(frame=copy.copy(frame), detection=frame_results["MPFaceDetection"][0]))
        
        if self._FACE_STUDIO_BLURRING:
            frame = frame_results["MPSegmentation"]
        if self._FACE_STUDIO_GRAY:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.merge([frame, frame, frame])

        return frame

    def draw_face_detection(self, frame, detection):

        h, w, _ = frame.shape  # Get the height and width of the image

        # Extract bounding box coordinates
        xmin = int(detection['relative_bounding_box']['xmin'] * w)
        ymin = int(detection['relative_bounding_box']['ymin'] * h)
        width = int(detection['relative_bounding_box']['width'] * w)
        height = int(detection['relative_bounding_box']['height'] * h)

        # Draw bounding box in green
        top_left = (xmin, ymin)
        bottom_right = (xmin + width, ymin + height)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Draw keypoints in red
        for idx, point in enumerate(detection['relative_keypoints']):
            x = int(point['x'] * w)
            y = int(point['y'] * h)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        return frame

# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================

# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTION
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================
if __name__ == "__main__":
    pass

# =============================================================================
