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

        self.segmentationModule = MPSegmentation(
            threshold=self._FACE_STUDIO_BLURRING_THRESH,
            bg_images_path="",
            bg_blur_ratio=(
                self._FACE_STUDIO_BLURRING_RATIO,
                self._FACE_STUDIO_BLURRING_RATIO,
            ),
        )

        self.mpFaceDetector = MPFaceDetection() 

        self.FaceSegmentation = Engine(
            show=False, 
            custom_objects=[
                self.segmentationModule, 
                self.mpFaceDetector, 
            ]
        )

    def process(self, frame):

        frame_results = self.FaceSegmentation.custom_processing(frame=frame)
        print(frame_results[1])

        if self._FACE_STUDIO_BLURRING:
            frame = frame_results[0]
            
        if self._FACE_STUDIO_GRAY:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.merge([frame, frame, frame])

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
