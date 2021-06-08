"""
Author: John Betacourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================
from utils import printlog, try_catch_log
import cv2
import numpy as np
import os

# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class VideoWriter:
    def __init__(
        self,
        file_path: str,
        file_name: str,
        rate: int = 30,
    ) -> None:
        """!
        Object class constructor for video captures
        @param file_path 'str' File path to write video
        @param file_name 'str' File name to save video
        @param rate 'int' Rate to write video (default: 30)
        @return None
        """

        # ---------------------------------------------------------------------
        # Video capture path variables
        self.file_name = f"{file_name}.avi"
        self.file_path = file_path
        self.file_dir = os.path.join(self.file_path, self.file_name)

        # Video capture object
        self.video_fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
        self.video_writer = None

        # Video capture features
        self.video_rate = rate
        self.video_width = None
        self.video_height = None
        self.ready = True

    def start(self, img: np.ndarray) -> None:
        """!
        Initializes video capture object
        @param img: 'cv2.math' image to be recorded in
                video capture. Its features will define
                the properties of the capture object.
        @return None
        """

        # Defines video writer properties
        self.video_width = img.shape[1]
        self.video_height = img.shape[0]

        # Check that path exits
        if not os.path.isdir(self.file_path):
            printlog(
                msg=f"path {self.file_path} created",
                msg_type="WARN",
            )
            os.mkdir(self.file_path)
        # Check that video file does not exits, if does, then remove it
        elif os.path.isfile(os.path.join(self.file_path, self.file_name)):
            os.remove(os.path.join(self.file_path, self.file_name))
            printlog(
                msg=f"previous video file {self.file_name} removed",
                msg_type="WARN",
            )

        self.video_writer = cv2.VideoWriter(
            self.file_dir,
            self.video_fourcc,
            self.video_rate,
            (self.video_width, self.video_height),
        )

        printlog(
            msg=f"{self.file_name} video file created, size:{self.video_width}X{self.video_height}, rate:{self.video_rate}",
            msg_type="INFO",
        )

    @try_catch_log
    def write(self, img: np.ndarray) -> None:
        """!
        Writes the next image whenever the VideoWritter
        is ready.
        @param img 'cv2.math' image to record in
                video capture
        @return None
        """

        # Starts the video writter object
        if self.video_writer is None:
            self.start(img=img)

        # Writes the image into the video
        self.video_writer.write(img)

    @try_catch_log
    def close(self) -> None:
        """!
        Closes video capture object
        @return None
        """
        if self.video_writer is not None:
            self.video_writer.release()


# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================

# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTION
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================