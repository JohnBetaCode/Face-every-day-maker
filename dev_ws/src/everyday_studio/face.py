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
from python_utils import printlog
import numpy as np


# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class FaceStudio:
    def __init__(self) -> None:
        """
        Initializes the FaceStudio class with configuration for face processing and image manipulation.

        This method sets up several processing parameters based on environment variables, including options for blurring, grayscale conversion, and face correction. It instantiates an Engine object with MPSegmentation and MPFaceDetection for performing face segmentation and detection within video frames.

        Attributes:
            _FACE_STUDIO_BLURRING_THRESH (float): Threshold for segmentation blurring, determining the sensitivity of the segmentation process. A higher value might result in more aggressive foreground-background separation.

            _FACE_STUDIO_BLURRING_RATIO (int): The ratio of blurring applied to the segmented image. Affects the smoothness of the blurred areas.

            _FACE_STUDIO_BLURRING (int): A flag indicating whether blurring should be applied to the segmented image (1 for true, 0 for false).

            _FACE_STUDIO_GRAY (int): A flag indicating whether the image should be converted to grayscale (1 for true, 0 for false).

            _FACE_CORRECT_RATIO (int): A flag indicating whether face aspect ratio correction should be applied (1 for true, 0 for false).

            _FACE_CORRECT_RATIO_FACTOR (float): The factor by which the face's aspect ratio is corrected. Influences how much the image is zoomed in or out around the face.

            _VIDEO_NAME (str): The name used for debug windows showing processed frames.

            _FACE_STUDIO_DEBUG_WINDOW (int): A flag indicating whether debug windows should be displayed (1 for true, 0 for false).

            FaceSegmentation (Engine): An Engine object configured with MPSegmentation and MPFaceDetection for processing the video frames.
        """
        self._FACE_STUDIO_BLURRING_THRESH = float(
            os.getenv("FACE_STUDIO_BLURRING_THRESH", default=0.5)
        )
        self._FACE_STUDIO_BLURRING_RATIO = int(
            os.getenv("FACE_STUDIO_BLURRING_RATIO", default=45)
        )
        self._FACE_STUDIO_BLURRING = int(os.getenv("FACE_STUDIO_BLURRING", default=1))
        self._FACE_STUDIO_GRAY = int(os.getenv("FACE_STUDIO_GRAY", default=1))

        # For face correction
        self._FACE_CORRECT_RATIO = int(os.getenv("FACE_CORRECT_RATIO", default=1))
        self._FACE_CORRECT_RATIO_FACTOR = float(
            os.getenv("FACE_CORRECT_RATIO_FACTOR", default=0.3)
        )

        self._VIDEO_NAME = os.getenv("VIDEO_NAME")

        self._FACE_STUDIO_DEBUG_WINDOW = int(
            os.getenv("FACE_STUDIO_DEBUG_WINDOW", default=1)
        )

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
                MPFaceDetection(),
            ],
        )

    def process(self, frame):
        """
        Processes a given frame with configured face detection, segmentation, and image enhancements.

        This method performs the following operations in sequence:
        1. Applies custom processing using the Engine object, which includes face detection and segmentation.
        2. Optionally displays a debug window with face detection results if enabled.
        3. Applies blurring to the frame if configured.
        4. Converts the frame to grayscale and back to a three-channel image if grayscale conversion is enabled.
        5. Applies face aspect ratio correction if enabled and relevant conditions are met (e.g., faces are detected).

        Parameters:
            frame (numpy.ndarray): The input video frame to be processed. It is expected to be in a format compatible with OpenCV operations.

        Returns:
            numpy.ndarray: The processed frame after applying the configured operations.

        Note:
            - The method makes defensive copies of the input frame before applying certain operations to preserve the original data.
            - Debugging windows, when enabled, are named according to the `_VIDEO_NAME` attribute and show the results of face detection.
            - Blurring and grayscale conversion are applied based on the respective flags set during initialization.
            - Face aspect ratio correction is only applied if exactly one face is detected in the frame, with warnings logged for other cases.
        """

        frame_results = self.FaceSegmentation.custom_processing(frame=copy.copy(frame))

        if self._FACE_STUDIO_DEBUG_WINDOW:
            frame_debug = self.draw_face_detection(
                frame=copy.copy(frame), detections=frame_results["MPFaceDetection"]
            )
            cv2.imshow(
                f"{self._VIDEO_NAME}-debug",
                frame_debug,
            )

        if self._FACE_STUDIO_BLURRING:
            frame = frame_results["MPSegmentation"]
        if self._FACE_STUDIO_GRAY:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.merge([frame, frame, frame])
        if self._FACE_CORRECT_RATIO:
            if len(frame_results["MPFaceDetection"]) > 1:
                printlog(msg="More than one face detected in frame", msg_type="WARN")
            if not len(frame_results["MPFaceDetection"]):
                printlog(msg="No faces detected in frame", msg_type="WARN")
            else:
                frame = self.correct_face_aspect_ratio(
                    frame=frame, face=frame_results["MPFaceDetection"][0]
                )

        return frame

    def draw_face_detection(self, frame, detections):
        """
        Draws bounding boxes and keypoints for detected faces on the provided frame.

        This method iterates over all detected faces provided in the `detections` list. For each detection,
        it calculates the bounding box coordinates based on the relative positions reported in the detection
        and the frame's dimensions. It then draws a green rectangle around the detected face and marks keypoints
        (e.g., eyes, nose, mouth) with red dots.

        Parameters:
            frame (numpy.ndarray): The video frame on which the face detections are to be drawn. The frame should
                                be in a format compatible with OpenCV (height x width x channels).
            detections (list): A list of dictionaries, each containing the detection results for a single face.
                            Expected keys include "relative_bounding_box" for the bounding box coordinates and
                            "relative_keypoints" for facial landmark positions, both relative to the frame size.

        Returns:
            numpy.ndarray: The same input frame with bounding boxes and keypoints drawn on it.

        Note:
            - The bounding boxes are drawn in green with a thickness of 2 pixels.
            - Facial keypoints are marked with red dots.
            - This method modifies the input frame in place but also returns it for convenience.
        """
        h, w, _ = frame.shape  # Get the height and width of the image

        for detection in detections:
            # Extract bounding box coordinates
            xmin = int(detection["relative_bounding_box"]["xmin"] * w)
            ymin = int(detection["relative_bounding_box"]["ymin"] * h)
            width = int(detection["relative_bounding_box"]["width"] * w)
            height = int(detection["relative_bounding_box"]["height"] * h)

            # Draw bounding box in green
            top_left = (xmin, ymin)
            bottom_right = (xmin + width, ymin + height)
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

            # Draw keypoints in red
            for idx, point in enumerate(detection["relative_keypoints"]):
                x = int(point["x"] * w)
                y = int(point["y"] * h)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        return frame

    def correct_face_aspect_ratio(self, frame, face):
        """
        Adjusts the aspect ratio of a detected face within the given frame by centering and zooming.

        This method calculates the center of the detected face and applies a translation to center the face
        within the frame. It then applies a zooming operation to adjust the size of the face based on a
        predefined ratio factor, aiming to normalize the appearance of faces across different frames.

        Parameters:
            frame (numpy.ndarray): The input video frame containing the detected face. The frame should
                                be in a format compatible with OpenCV operations (height x width x channels).
            face (dict): A dictionary containing the detection information of the face, including
                        "relative_bounding_box" which specifies the bounding box of the face relative
                        to the frame size.

        Returns:
            numpy.ndarray: The frame after applying the translation and zooming operations to adjust
                        the face's aspect ratio.

        Note:
            - The translation is determined by calculating the offset required to center the face's
            bounding box within the frame.
            - The zoom factor is calculated based on the face's width relative to a predefined ratio
            factor (`_FACE_CORRECT_RATIO_FACTOR`), aiming to standardize the size of faces across frames.
            - This method may alter the composition of the frame significantly, especially if the
            detected face is initially far from the center or very large/small compared to the frame size.
        """
        box_ct_x = (
            face["relative_bounding_box"]["xmin"]
            + face["relative_bounding_box"]["width"] * 0.5
        )
        box_ct_y = (
            face["relative_bounding_box"]["ymin"]
            + face["relative_bounding_box"]["height"] * 0.5
        )

        # Set the translation distances in pixels
        tx = int(frame.shape[1] * (0.5 - box_ct_x))  # Move right by 100 pixels
        ty = int(frame.shape[0] * (0.5 - box_ct_y))  # Move down by 50 pixels

        # Define the translation matrix
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])

        # Use warpAffine to transform the image using the translation matrix
        translated_image = cv2.warpAffine(
            frame, translation_matrix, (frame.shape[1], frame.shape[0])
        )

        translated_image = self.zoom_image(
            frame=translated_image,
            zoom_factor=self._FACE_CORRECT_RATIO_FACTOR
            / face["relative_bounding_box"]["width"],
        )

        return translated_image

    def zoom_image(self, frame, zoom_factor):
        """
        Applies zooming to an image based on the specified zoom factor.

        This method creates a scaling matrix to zoom in or out on the center of the frame. The zoom factor
        determines how much the image is enlarged or reduced. A zoom factor greater than 1 zooms in on the
        image, making objects appear larger, while a zoom factor less than 1 zooms out, making objects appear
        smaller. The method uses affine transformation to apply the zoom, maintaining the original image dimensions.

        Parameters:
            frame (numpy.ndarray): The input image to be zoomed. The image should be in a format compatible
                                with OpenCV operations, typically height x width x channels.
            zoom_factor (float): The factor by which the image should be zoomed. Values greater than 1.0
                                will zoom in on the image, while values less than 1.0 will zoom out.

        Returns:
            numpy.ndarray: The zoomed image with the same dimensions as the input frame.

        Note:
            - The zoom is centered around the middle of the image, ensuring that the zoom effect is uniformly
            applied in all directions.
            - The border mode is set to `cv2.BORDER_REFLECT` to handle the borders of the zoomed image, reflecting
            the edge pixels to fill any space that would otherwise be left empty by the zoom operation.
        """

        height, width = frame.shape[:2]

        # Center of the image
        center_x, center_y = width / 2, height / 2

        # Scaling matrix
        scaling_matrix = np.array(
            [
                [zoom_factor, 0, (1 - zoom_factor) * center_x],
                [0, zoom_factor, (1 - zoom_factor) * center_y],
            ],
            dtype=np.float32,
        )

        # Apply the affine transformation (scaling)
        zoomed_img = cv2.warpAffine(
            frame, scaling_matrix, (width, height), borderMode=cv2.BORDER_REFLECT
        )

        return zoomed_img


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
