"""
Author: John Betacourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================
import os
import cv2
from datetime import datetime

from utils import try_catch_log

# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================


class File(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self.isfile = os.path.isfile(self.path)

    @property
    def extension(self):
        return os.path.splitext(self.path)[1] if self.isfile else None

    @property
    def name(self):
        return os.path.basename(self.path).split(".")[0] if self.isfile else None

    @property
    def created_date(self):
        return (
            datetime.fromtimestamp(os.path.getctime(self.path)) if self.isfile else None
        )

    @property
    def modified_date(self):
        return (
            datetime.fromtimestamp(os.path.getmtime(self.path)) if self.isfile else None
        )


class Image(File):
    def __init__(self, path: str, load: bool = False) -> None:

        File.__init__(self, path=path)

        self.image = None

        # If the file exist load the image
        if self.isfile and load:
            self.load()

    @try_catch_log
    def load(self) -> None:
        self.image = cv2.imread(self.path)

    @property
    def width(self) -> int:
        return self.image.shape[0] if self.image is not None else 0

    @property
    def height(self) -> int:
        return self.image.shape[1] if self.image is not None else 0

    @property
    def channels(self) -> int:
        return self.image.shape[2] if self.image is not None else 0


# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================
def get_files_names(folder: str = "", extensions: tuple = ()) -> list:
    """! Returns all files discriminated by extension in a folder
    @param folder (str) folder to search for files
    @param extensions (tuple) file extensions tuple/list to discrimanated files
    @return list with all file names in folder argument
    """
    return [file for file in os.listdir(folder) if file.endswith(extensions)]


def get_sub_folders(folder: str = "") -> list:
    return [f.path for f in os.scandir(folder) if f.is_dir()]


# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTION
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================
if __name__ == "__main__":

    files = {
        sub_folder: get_files_names(folder=sub_folder, extensions=(".jpg", ".png"))
        for sub_folder in get_sub_folders(folder="/workspace/dev_ws/media/images/")
    }

# =============================================================================