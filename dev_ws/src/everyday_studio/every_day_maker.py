# =============================================================================
"""
Author: John Betacourt Gonzalez
Aka: @JohnBetaCode
"""

# =============================================================================
# LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPENDENCIES - LIBRARIES AND DEPEN
# =============================================================================
import operator
import os

import cv2
import numpy as np
import math

from tqdm import tqdm
from face import Face, FaceDetector
from capture import VideoWriter
from file_utils import Image, get_files_names, get_sub_folders
from utils import printlog, try_catch_log, print_text_list


# =============================================================================
# CLASSES - CLASSES - CLASSES - CLASSES - CLASSES - CLASSES  - CLASSES - CLASSE
# =============================================================================
class DataSet:
    def __init__(self, path: str = "") -> None:
        """!
        Constructor for dataset class instances
        @param path 'string' absolute path to the dataset
        """

        self.path = path

        self.idx = 0

        self.data_files = None
        self.data_values = None

        self.data_extensions = (".jpg", ".png")

        self.idx_img = None

        if path != "":
            self.load(path=self.path)

    def goto_next(self) -> None:
        """!
        go to next dataset index/sample if is valid do it
        """

        if self.data_values is not None:
            if self.idx < len(self.data_values) - 1:
                self.idx += 1
                self.goto_idx(idx=self.idx, print_info=True)
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
                self.goto_idx(idx=self.idx, print_info=True)
            else:
                printlog(msg="minimum idx limit", msg_type="WARN")
        else:
            printlog(msg="No dataset loaded", msg_type="WARN")

    def goto_last(self) -> None:
        """!
        go to the last dataset index
        """
        self.goto_idx(idx=int(len(self.data_values) - 1), print_info=True)

    def goto_idx(self, idx: int, print_info: bool = False) -> None:
        """!
        from specified idx moves assing a new one and load new file sample
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

    @try_catch_log
    def load(self, path: str) -> None:
        """!
        loads the dataset from a specified path
        @param path 'string' absolute path to the dataset
        """

        # check if the path given is valid or not
        if not os.path.isdir(path):
            printlog(msg=f"invalid path {path}", msg_type="WARN")
            return

        # load dataset as subfolders and files
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
            self.goto_idx(idx=self.idx)

    def __str__(self):
        """!
        Get object instace string for printings
        @return str_ 'string' string with object instance info
        """

        if self.data_files is None and self.path == "":
            return "no data loaded"
        elif self.data_files is None:
            return f"no dataset found in {self.path}"

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
        return len(self.data_values)


class Studio:
    def __init__(self) -> None:
        """!
        Constructor for every day studio instance
        """

        # ---------------------------------------------------------------------``
        # instancite face detector object
        self._PREVISUALIZE_FACE_CORRECTION = int(
            os.getenv("PREVISUALIZE_FACE_CORRECTION", default=1)
        )
        self._face_detector = FaceDetector(
            predictor_path=os.path.join(
                os.getenv("CONFIGS_PATH"), os.getenv("PREDICTOR_NAME")
            )
        )
        self.face = None

        # ---------------------------------------------------------------------
        # instancite of video capture/recorder
        self._EXPORT_PATH = os.getenv("VIDEO_PATH", default="/workspace/dev_ws/export")
        self._EXPORT_VIDEO_NAME = os.getenv("VIDEO_NAME", default="every_day")
        self._video_capture = VideoWriter(
            file_path=self._EXPORT_PATH,
            file_name=self._EXPORT_VIDEO_NAME,
            rate=int(os.getenv("VIDEO_RATE", default=30)),
        )

        # ---------------------------------------------------------------------
        # instancite dataset detector object
        self.dataset = DataSet(path=os.getenv("DATASET_PATH"))

        # ---------------------------------------------------------------------
        # window properties
        self._WIN_NAME = os.getenv("WIN_NAME", default="every_day_studio")
        self._WIN_WIDTH = int(os.getenv("WIN_WIDTH", default=640))
        self._WIN_HEIGHT = int(os.getenv("WIN_HEIGHT", default=360))
        self._WIN_TIME = int(os.getenv("WIN_TIME", default=-1))

        # video properties
        self._VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", default=640))
        self._VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", default=360))
        self._VIDEO_EXPORT_GRAY = int(os.getenv("VIDEO_EXPORT_GRAY", default=1))
        self._VIDEO_EXPORT_VISUALS = int(os.getenv("VIDEO_EXPORT_VISUALS", default=1))
        self._VIDEO_EXPORT_PREVISUALIZATION = int(
            os.getenv("VIDEO_EXPORT_PREVISUALIZATION", default=1)
        )

        # Other constans and variables
        self._MEDIA_PATH = os.getenv("MEDIA_PATH")

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
            "c": {1048675, 1179715},
            "v": {1048694, 1179734},
            "b": {1048674, 1179714},
            "n": {1048686, 1114085},
            "m": {1048685, 1179725},
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

                    # Inference with face detector and check for face in image
                    self.face = self._face_detector.predict(img=idx_img)
                    if self.face is None:
                        printlog(
                            msg="No face detected in image sample", msg_type="WARN"
                        )
                    else:
                        idx_img = self._face_detector.visualize_landmarks(
                            img=idx_img, face=self.face
                        )
                        if self._PREVISUALIZE_FACE_CORRECTION:
                            cv2.imshow(
                                f"{self._WIN_NAME}_FACE_CORRECTION",
                                self.get_face_img_corrected(
                                    img=self.dataset.idx_img.get_data(
                                        size=(self._VIDEO_WIDTH, self._VIDEO_HEIGHT)
                                    ),
                                    face=self.face,
                                    visuals=True,
                                ),
                            )
                else:
                    idx_img = np.zeros(
                        (self._VIDEO_WIDTH, self._VIDEO_HEIGHT, 3), np.uint8
                    )
            except Exception as e:
                printlog(msg=e, msg_type="ERROR")
                idx_img = np.zeros((self._VIDEO_WIDTH, self._VIDEO_HEIGHT, 3), np.uint8)

            cv2.imshow(
                self._WIN_NAME,
                self.draw_visuals(
                    img=cv2.resize(
                        idx_img,
                        (self._WIN_WIDTH, self._WIN_HEIGHT),
                        int(cv2.INTER_NEAREST),
                    )
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
            return

        printlog(msg="stating video recorder\n", msg_type="INFO")

        # rocord every frame or video
        for idx_data in tqdm(range(len(self.dataset.data_values))):

            try:
                # go to index
                self.dataset.goto_idx(idx=idx_data)

                # Check that the current sample has data
                if self.dataset.idx_img is not None and self.dataset.idx_img.isfile:

                    # get current idx dataset image
                    idx_img = self.dataset.idx_img.get_data(
                        size=(self._VIDEO_WIDTH, self._VIDEO_HEIGHT)
                    )

                    # Inference with face detector and check for face in image
                    self.face = self._face_detector.predict(img=idx_img)
                    if self.face is None:
                        printlog(
                            msg=f"skyping image {self.dataset.idx_img.name}, no face detected",
                            msg_type="WARN",
                        )
                        continue
                    else:
                        idx_img = self._face_detector.visualize_landmarks(
                            img=idx_img, face=self.face
                        )
                        idx_img = self.get_face_img_corrected(
                            img=self.dataset.idx_img.get_data(
                                size=(self._VIDEO_WIDTH, self._VIDEO_HEIGHT)
                            ),
                            face=self.face,
                            visuals=self._VIDEO_EXPORT_VISUALS,
                            exp_gray=self._VIDEO_EXPORT_GRAY,
                        )
                else:
                    printlog(
                        msg=f"skyping image {self.dataset.idx_img.name}, file no found",
                        msg_type="WARN",
                    )
                    continue
            except Exception as e:
                printlog(
                    msg=f"skyping image {self.dataset.idx_img.name}, error:{e}",
                    msg_type="ERROR",
                )
                continue

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
                    printlog(msg="video creation process canceled", msg_type="WARN")
                    self.dataset.goto_idx(idx=current_idx)
                    return

        # concatenate audio
        audio_src = os.getenv("AUDIO_TRACK", default=None)
        if record_audio and audio_src is not None:
            audio_src_path = os.path.join(self._MEDIA_PATH, "sound", audio_src)
            if os.path.isfile(audio_src_path):
                printlog(msg="\nadding audio to video", msg_type="INFO")
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

    def draw_visuals(self, img: np.array) -> np.array:
        """! draw studio visuals and data info in image
        @param img 'np.array' image to draw visuals
        @return img 'np.array' image with visuals drawn
        """

        img = print_text_list(
            img=img,
            tex_list=[
                f"idx: {self.dataset.idx}/{self.dataset.len}",
                f"file: {self.dataset.idx_img.name}.{self.dataset.idx_img.extension}",
                f"date creation: {self.dataset.idx_img.created_date}",
                f"date modified: {self.dataset.idx_img.modified_date}",
                f"size: {self.dataset.idx_img.width}x{self.dataset.idx_img.height}x{self.dataset.idx_img.channels}",
            ],
            color=(255, 255, 255),
            orig=(10, 25),
            fontScale=0.5,
            y_jump=23,
        )

        return img

    def get_face_img_corrected(
        self, img: np.array, face: Face, exp_gray: bool = False, visuals: bool = False
    ) -> np.array:
        """!
        Center and align a image respect to a face components
        @param img 'np.array' image to center and align
        @param face 'Face' face components to align image
        @param exp_gray 'bool' export result in gray scale
        @param visuals 'bool' print visuals in image result
        @return img 'np.array' image centered and aligned respect with face
        """

        # ------------------------------------------------------------------
        img = (
            img
            if not exp_gray
            else cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        )

        if visuals:
            img = self._face_detector.visualize_landmarks(img=img, face=face)
            cv2.line(
                img,
                tuple(face.left_eye[3]),
                tuple(face.right_eye[0]),
                (255, 255, 255),
                1,
            )

        # ------------------------------------------------------------------
        # Center and align image

        dx = img.shape[1] // 2 - face.nose[2][0]
        dy = img.shape[0] // 2 - face.nose[2][1]
        cnt_pt = (img.shape[1] // 2, img.shape[0] // 2)
        M = np.float32(
            [
                [1, 0, dx],
                [0, 1, dy],
            ]
        )
        img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

        # ------------------------------------------------------------------
        # Calculate angle to rate
        angle = math.degrees(
            math.atan2(
                face.left_eye[3][1] - face.right_eye[0][1],
                face.left_eye[3][0] - face.right_eye[0][0],
            )
        )

        # Calculate resizing factor
        len_scale = np.sqrt(
            (face.left_eye[3][1] - face.right_eye[0][1]) ** 2
            + (face.left_eye[3][0] - face.right_eye[0][0]) ** 2
        )
        scale = 1.0 + (1.0 - len_scale / 150.0)

        # Find trans formation matrix
        M = cv2.getRotationMatrix2D(center=cnt_pt, angle=angle, scale=scale)
        img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

        if visuals:
            cv2.circle(img, (img.shape[1] // 2, img.shape[0] // 2), 1, (0, 0, 255), -1)

        return img

    def get_report(self) -> str:
        return ""

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
            + f"\tM: go to previous sample\n"
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
