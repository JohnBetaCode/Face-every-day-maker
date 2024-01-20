# =============================================================================
"""
Author: John Betancourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================
import operator
import os
import cv2
import numpy as np

from tqdm import tqdm
from capture import VideoWriter
from python_utils import printlog, try_catch_log, print_text_list
from face import FaceStudio
from file_utils import Image, get_files_names, get_sub_folders


# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class DataSet:
    def __init__(self, path: str = "") -> None:
        """!
        Constructor for dataset class instances
        @param path 'string' absolute path to the dataset
        """

        self._PRINT_IMG_INFO = int(os.getenv("PRINT_IMG_INFO", default=1))

        self.path = path

        self.idx = 0
        self.idx_img = None

        self.data_files = None
        self.data_values = None
        self.data_extensions = (".jpg", ".JPG", ".png", ".PNG")

        if self.path != "":
            self.load(path=self.path)

    def goto_next(self) -> None:
        """!
        go to next dataset index/sample if is valid do it
        """

        if self.data_values is not None:
            if self.idx < len(self.data_values) - 1:
                self.idx += 1
                self.goto_idx(idx=self.idx, print_info=self._PRINT_IMG_INFO)
            else:
                printlog(msg="idx exceed limit", msg_type="WARN")
        else:
            printlog(msg="No dataset loaded", msg_type="WARN")

    def goto_previous(self) -> None:
        """!
        go to previous dataset index/sample if is valid do it
        """

        if self.data_values is not None:
            if self.idx > 0:
                self.idx -= 1
                self.goto_idx(idx=self.idx, print_info=self._PRINT_IMG_INFO)
            else:
                printlog(msg="minimum idx limit", msg_type="WARN")
        else:
            printlog(msg="No dataset loaded", msg_type="WARN")

    def goto_last(self) -> None:
        """!
        go to the last dataset index
        """
        self.goto_idx(
            idx=int(len(self.data_values) - 1), print_info=self._PRINT_IMG_INFO
        )

    def goto_idx(self, idx: int, print_info: bool = False) -> None:
        """!
        from specified idx moves assign a new one and load new file sample
        @param idx 'int' index to go to sample
        @param print_info 'bool' show data info
        """

        if self.data_values is not None:
            if idx >= 0 or idx < len(self.data_values):
                # Asssing new index
                self.idx = idx

                # Create new image from dataset index
                self.idx_img = Image(path=self.data_values[self.idx].path)
                self.idx_img.load(print_info=print_info)

        else:
            self.idx_img = None
            printlog(msg="No dataset loaded", msg_type="WARN")

    def load(self, path: str) -> None:
        """!
        loads the dataset from a specified path
        @param path 'string' absolute path to the dataset
        """

        # check if the path given is valid or not
        if not os.path.isdir(path):
            printlog(msg=f"invalid path {path}", msg_type="WARN")
            return

        # load dataset as subfolder and files
        self.data_files = {
            sub_folder: get_files_names(
                folder=sub_folder, extensions=self.data_extensions
            )
            for sub_folder in get_sub_folders(folder=self.path)
        }

        # Load dataset as images & file properties
        self.data_values = [
            Image(
                path=os.path.join(sub_folder, file_name),
                load=False,
            )
            for sub_folder, files_in_sub in self.data_files.items()
            for file_name in files_in_sub
        ]

        # order list by timestamp of time creation
        self.data_values = sorted(
            self.data_values, key=operator.attrgetter("modified_date_stamp")
        )

        # go to the first index of the dataset
        if len(self.data_values):
            self.idx = len(self.data_values) - 1
            self.goto_idx(idx=self.idx, print_info=self._PRINT_IMG_INFO)

    def __str__(self):
        """!
        Get object instantiate string for printings
        @return str_ 'string' string with object instance info
        """

        if self.data_files is None and self.path == "":
            return "not data loaded"
        elif self.data_files is None:
            return f"not dataset found in {self.path}"

        str_ = f"\nData set loaded from {self.path} \n\n"
        files_cnt = 0

        for sub_folder, data_list in self.data_files.items():
            sub_folder_name = sub_folder.split("/")[-1]
            str_ += f"\t{sub_folder_name}: {len(data_list)}\n"
            files_cnt += len(data_list)
        str_ += f"\n\t\ttotal: {files_cnt}\n"

        return str_

    @property
    def sub_folders_name(self) -> list:
        return self.data_files.keys() if self.data_files is not None else []

    @property
    def len(self) -> int:
        return len(self.data_values) if self.data_values is not None else 0


class Studio:
    def __init__(self) -> None:
        """!
        Constructor for every day studio instance
        """

        # ---------------------------------------------------------------------
        self._DEBUG_LEVEL = int(os.getenv("DEBUG_LEVEL", default=1))

        # window properties
        self._WIN_NAME = os.getenv("WIN_NAME", default="every_day_studio")
        self._WIN_WIDTH = int(os.getenv("WIN_WIDTH", default=640))
        self._WIN_HEIGHT = int(os.getenv("WIN_HEIGHT", default=360))
        self._WIN_TIME = int(os.getenv("WIN_TIME", default=-1))

        # video properties
        self._VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", default=640))
        self._VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", default=360))
        self._VIDEO_EXPORT_VISUALS = int(os.getenv("VIDEO_EXPORT_VISUALS", default=1))
        self._VIDEO_EXPORT_PREVISUALIZATION = int(
            os.getenv("VIDEO_EXPORT_PREVISUALIZATION", default=1)
        )
        self._VIDEO_EXPORT_DATE = int(os.getenv("VIDEO_EXPORT_DATE", default=1))

        self._EXPORT_PATH = os.getenv("VIDEO_EXPORT_PATH")
        self._EXPORT_VIDEO_NAME = os.getenv("VIDEO_NAME")

        # Other constant and variables
        self._MEDIA_PATH = os.getenv("MEDIA_PATH")
        self._AUDIO_PATH = os.getenv("AUDIO_PATH")

        # ---------------------------------------------------------------------s
        # Face studio for operations
        self.face_studio = FaceStudio()

        # ---------------------------------------------------------------------
        # instance dataset detector object
        self.dataset = DataSet(path=self._MEDIA_PATH)

        # ---------------------------------------------------------------------
        # Video Writer Object
        self._video_capture = VideoWriter(
            file_path=self._EXPORT_PATH,
            file_name=self._EXPORT_VIDEO_NAME,
            rate=int(os.getenv("VIDEO_RATE", default=30)),
        )

    @try_catch_log
    def cb_key_event(self, key) -> None:
        """!
        Get and execute action from users key
        @param key 'int' keyboard actions
        """

        key2code = {
            "1": {1048625, 1179697},
            "2": {1048626, 1179698},
            "3": {1048627, 1179699},
            "4": {1048628, 1179700},
            "5": {1048629, 1179701},
            "6": {1048630, 1179702},
            "7": {1048631, 1179703},
            "8": {1048632, 1179704},
            "9": {1048633, 1179705},
            "0": {1048624, 1179696},
            "q": {1048689, 1179729, 113},
            "w": {1048695, 1179735, 119},
            "e": {1048677, 1179717, 101},
            "r": {1048690, 1179730, 114},
            "t": {1048692, 1179732, 116},
            "y": {1048697, 1179737},
            "u": {1048693, 1179733},
            "i": {1048681, 1179721},
            "o": {1048687, 1179727},
            "p": {1048688, 1179728},
            "a": {1048673, 1179713, 97},
            "s": {1048691, 1179731, 115},
            "d": {1048676, 1179716, 100},
            "f": {1048678, 1179718, 102},
            "g": {1048679, 1179719, 103},
            "h": {1048680, 1179720, 104},
            "j": {1048682, 1179722},
            "k": {1048683, 1179723},
            "l": {1048684, 1179724},
            "ñ": {1048817, 1179857},
            "z": {1048698, 1179708, 122},
            "x": {1048696, 1179736},
            "c": {1048675, 1179715, 99},
            "v": {1048694, 1179734},
            "b": {1048674, 1179714, 98},
            "n": {1048686, 1114085, 110},
            "m": {1048685, 1179725, 109},
            "up arrow": {1245010, 1113938},
            "right arrow": {1245011, 1113939, 65361},
            "left arrow": {1245009, 1113937, 65363},
            "down arrow": {1245012, 1113940},
            "space bar": {1179680, 1048608},
        }

        # If pressed No key then continue
        if key == -1:
            pass
        # If pressed H/h key then print help
        elif key in key2code["h"]:
            print(self.shortcuts, flush=True)
        # If pressed Q/q key then quit program
        elif key in key2code["q"]:
            exit(1)
        # If pressed N/n key then next sample/image
        elif key in key2code["n"]:
            self.dataset.goto_next()
        # If pressed B/b key then previous sample/image
        elif key in key2code["b"]:
            self.dataset.goto_previous()
        # If pressed M/m key then go to last sample/image
        elif key in key2code["m"]:
            self.dataset.goto_last()
        # If pressed C/c key then create/export video
        elif key in key2code["c"]:
            self.export_video()
        # If pressed no key defined then print message
        else:
            printlog(msg=f"{key} key action no defined", msg_type="WARN")
            return

    @try_catch_log
    def run(self) -> None:
        """! function can be used for threading or just the loop
        of graphics for the every day studio
        @return _ 'None'
        """

        # Print help menu
        print(self.shortcuts)

        while True:
            try:
                # Check that the current sample has data
                if self.dataset.idx_img is not None and self.dataset.idx_img.isfile:
                    # get current idx dataset image
                    idx_img = self.dataset.idx_img.get_data(
                        size=(self._VIDEO_WIDTH, self._VIDEO_HEIGHT)
                    )
                    idx_img = self.face_studio.process(frame=idx_img)

                else:
                    idx_img = np.zeros(
                        (self._VIDEO_WIDTH, self._VIDEO_HEIGHT, 3), np.uint8
                    )

            except Exception as e:
                printlog(msg=e, msg_type="ERROR")
                idx_img = np.zeros((self._VIDEO_WIDTH, self._VIDEO_HEIGHT, 3), np.uint8)

            cv2.imshow(
                self._WIN_NAME,
                cv2.resize(
                    idx_img,
                    (self._WIN_WIDTH, self._WIN_HEIGHT),
                    int(cv2.INTER_NEAREST),
                ),
            )
            self.cb_key_event(key=cv2.waitKeyEx(self._WIN_TIME))

    @try_catch_log
    def export_video(self, record_audio: bool = True) -> None:
        """! export everyday video to folder and file specified in
        video recorder constructor (self._video_capture)
        @param record_audio 'bool' enable/disable audio export in video
        @return _ 'None'
        """

        if self._VIDEO_EXPORT_PREVISUALIZATION:
            printlog(
                msg="video exportation pre-visualization slow down the process",
                msg_type="WARN",
            )

        # save current index for later return to it
        current_idx = self.dataset.idx

        # If there's no dataset
        if self.dataset.data_values is None:
            printlog(msg="No data to export video", msg_type="ERROR")
            return

        printlog(msg="starting video recorder ...", msg_type="WARN")

        # record every frame or video
        iterator = tqdm(range(len(self.dataset.data_values)))
        for idx_data in iterator:
            try:
                # go to index
                self.dataset.goto_idx(idx=idx_data)

                # Check that the current sample has data
                if self.dataset.idx_img is not None and self.dataset.idx_img.isfile:
                    # printlog(msg=self.dataset.idx_img.name, msg_type="DEBUG")

                    # get current idx dataset image
                    idx_img = self.dataset.idx_img.get_data(
                        size=(self._VIDEO_WIDTH, self._VIDEO_HEIGHT)
                    )

                    # Inference with face detector and check for face in image
                    idx_img = self.face_studio.process(frame=idx_img)

                else:
                    printlog(
                        msg=f"skipping image {self.dataset.idx_img.name}, file no found",
                        msg_type="ERROR",
                    )
                    continue
            except Exception as e:
                printlog(
                    msg=f"skipping image {self.dataset.idx_img.name}, error:{e}",
                    msg_type="ERROR",
                )
                continue

            if self._VIDEO_EXPORT_DATE:
                pass
            
            # Write image to video capture
            self._video_capture.write(img=idx_img)

            if self._VIDEO_EXPORT_PREVISUALIZATION:
                cv2.imshow(
                    f"{self._WIN_NAME}_FACE_CORRECTION",
                    print_text_list(
                        img=cv2.resize(
                            idx_img,
                            (self._WIN_WIDTH, self._WIN_HEIGHT),
                            int(cv2.INTER_NEAREST),
                        ),
                        tex_list=["Exporting ...", "C: to cancel"],
                        color=(0, 0, 255),
                        orig=(10, 25),
                        fontScale=0.7,
                        y_jump=23,
                    ),
                )
                if cv2.waitKey(10) in [69, 99]:
                    printlog(
                        msg="The video creation process was canceled", msg_type="WARN"
                    )
                    self.dataset.goto_idx(idx=current_idx)
                    return

        # concatenate audio
        audio_src = os.getenv("AUDIO_TRACK", default=None)
        if record_audio and audio_src is not None:
            audio_src_path = os.path.join(self._AUDIO_PATH, audio_src)
            if os.path.isfile(audio_src_path):
                printlog(msg="Adding audio to video ...", msg_type="INFO")
                merge_audio_command = "ffmpeg -hide_banner -loglevel panic -y -i {src_path} -i {audio_src} -af apad -map 0:v -map 1:a -c:v copy -shortest {dst_path}".format(
                    src_path=self._video_capture.file_dir,
                    audio_src=audio_src_path,
                    dst_path=f"{self._EXPORT_PATH}/{self._EXPORT_VIDEO_NAME}.mp4",
                )
                os.system(merge_audio_command)
                os.remove(self._video_capture.file_dir)
            else:
                printlog(
                    msg=f"no audio source {audio_src} in {self._MEDIA_PATH}",
                    msg_type="ERROR",
                )

        printlog(msg="video recorder finished", msg_type="OKGREEN")

        # return to the previous index
        self.dataset.goto_idx(idx=current_idx)

    @property
    def shortcuts(self) -> str:
        """! Returns all options aviable from the studio window
        @return str_ 'string' of shortcuts list and help
        """
        str_ = (
            f"\nOptions:\n"
            + f"\tH: show help menu\n"
            + f"\tN: go to next sample\n"
            + f"\tB: go to previous sample\n"
            + f"\tM: go to last sample\n"
            + f"\tC: create/export video\n"
            + f"\tQ: quit\n"
        )
        return str_


# =============================================================================
# FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS  - FUNCTIONS - FUNC
# =============================================================================

# =============================================================================
# MAIN FUNCTION - MAIN FUNCTION - MAIN FUNCTION - MA[-IN FUNCTION - MAIN FUNCTI
# IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IMPLEMENTATION EXAMPLE - IM
# =============================================================================
if __name__ == "__main__":
    # Create instance of everyday studio
    day_studio = Studio()
    day_studio.run()

# =============================================================================
