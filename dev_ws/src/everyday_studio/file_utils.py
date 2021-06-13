"""
Author: John Betacourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================
from utils import printlog
import os
from datetime import datetime

import cv2

from utils import try_catch_log

# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================


class File(object):
    def __init__(self, path: str) -> None:
        """!
        Constructor for File class instances
        @param path 'string' absolute path to the file
        constructor instance
        """

        self.path = path
        self.isfile = os.path.isfile(self.path)

    @property
    def extension(self):
        """!
        @return _ 'string' file's extension
        """
        return os.path.splitext(self.path)[1] if self.isfile else None

    @property
    def name(self) -> str:
        """!
        @return _ 'string' file's name
        """
        return os.path.basename(self.path).split(".")[0] if self.isfile else ""

    @property
    def created_date(self):
        """!
        @return _ 'date' file's creation date
        """
        return (
            datetime.fromtimestamp(os.path.getctime(self.path)) if self.isfile else None
        )

    @property
    def created_date_stamp(self) -> float:
        """!
        @return _ 'float' timestamp of file's creation file
        """
        return os.path.getctime(self.path) if self.isfile else 0.0

    @property
    def modified_date(self):
        """!
        @return _ 'date' file's modification date
        """
        return (
            datetime.fromtimestamp(os.path.getmtime(self.path)) if self.isfile else None
        )

    @property
    def modified_date_stamp(self) -> float:
        """!
        @return _ 'float' timestamp of file's modification date
        """
        return os.path.getmtime(self.path) if self.isfile else 0.0


class Image(File):
    def __init__(self, path: str, load: bool = False) -> None:
        """!
        Constructor for Image class instances
        @param path 'string' absolute path to the Image
        @param load 'bool' load or not image data from
        constructor instance
        """

        File.__init__(self, path=path)

        self.image = None

        # If the file exist load the image
        if self.isfile and load:
            self.load(print_info=False)

    @try_catch_log
    def load(self, print_info: bool = True) -> None:
        """!
        load image data from file's path
        @param print_info 'bool' print image information
        to the std output
        """
        self.image = cv2.imread(self.path)
        if print_info:
            print(self)

    @property
    def width(self) -> int:
        """!
        @return width 'int' image width
        """
        return self.image.shape[0] if self.image is not None else 0

    @property
    def height(self) -> int:
        """!
        @return height 'int' image height
        """
        return self.image.shape[1] if self.image is not None else 0

    @property
    def channels(self) -> int:
        """!
        @return channels 'int' quantity of image channels
        """
        return self.image.shape[2] if self.image is not None else 0

    def get_data(self, size: tuple = ()):
        """!
        Get image data
        @param size 'tuple' new size to give image data
        """

        if not self.isfile:
            printlog(msg=f"no file {self.name} to get data", msg_type="ERROR")
            return None
        elif self.image is None:
            printlog(msg=f"no data loaded yet from {self.name}", msg_type="ERROR")
            return None
        elif not len(size):
            return self.image
        else:
            return cv2.resize(src=self.image, dsize=size)

    def __str__(self):
        """!
        Get object instace string for printings
        @return str_ 'string' string with object instance info
        """
        str_ = (
            f"\n\npath: {self.path}\n"
            + f"\tisfile: {self.isfile}\n"
            + f"\tname: {self.name}\n"
            + f"\text: {self.extension}\n"
            + f"\tcreation date: {self.created_date}\n"
            + f"\tmodified date: {self.modified_date}\n"
            + f"\tcreation date stamp: {self.created_date_stamp}\n"
            + f"\tmodified date stamp: {self.modified_date_stamp}\n"
            + f"\toriginal width: {self.width}\n"
            + f"\toriginal height: {self.height}\n"
            + f"\tchannels: {self.channels}\n"
        )
        return str_


# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================
def get_files_names(folder: str = "", extensions: tuple = ()) -> list:
    """! Returns all files discriminated by extension in a folder
    @param folder (str) folder to search for files
    @param extensions (tuple) file extensions tuple/list to discrimanated files
    @return _ 'list' list with all file names in folder argument
    """
    return [file for file in os.listdir(folder) if file.endswith(extensions)]


def get_sub_folders(folder: str = "") -> list:
    """! Returns all subfolders in a folder
    @param folder (str) folder to search for subfolders
    @return _ 'list' list with all subfolders name in the path specified at folder variable
    """
    return [f.path for f in os.scandir(folder) if f.is_dir()]


# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTION
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================
if __name__ == "__main__":

    # Get files from absolute path and its subfolders contents
    files = {
        sub_folder: get_files_names(folder=sub_folder, extensions=(".jpg", ".png"))
        for sub_folder in get_sub_folders(folder="/workspace/dev_ws/media/images/")
    }

    # Loads an image
    test_img = Image(path="/workspace/dev_ws/src/facial_features/images/image_1.jpg")
    print(test_img)

# =============================================================================
