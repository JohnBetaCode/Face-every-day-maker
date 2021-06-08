#!/usr/bin/env python3
# =============================================================================
"""
Code Information:
    Programmer: Eng. John Alberto Betancourt G
"""

# =============================================================================
import inspect
import math
import os

import cv2

# =============================================================================
import numpy as np

# =============================================================================
# VISUAL - VISUAL - VISUAL - VISUAL - VISUAL - VISUAL - VISUAL - VISUAL - VISUA


class bcolors:
    """!
    Class for defining the color used by the printlog function
    """

    LOG = {
        "WARN": ["\033[93m", "WARN"],
        "ERROR": ["\033[91m", "ERROR"],
        "OKGREEN": ["\033[32m", "INFO"],
        "OKPURPLE": ["\033[35m", "INFO"],
        "INFO": ["\033[0m", "INFO"],  # ['\033[94m', "INFO"],
        "BOLD": ["\033[1m", "INFO"],
        "GRAY": ["\033[90m", "INFO"],
    }
    BOLD = "\033[1m"
    ENDC = "\033[0m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    GRAY = "\033[90m"
    UNDERLINE = "\033[4m"


def printlog(
    msg: str,
    msg_type: str = "INFO",
    flush: bool = True,
    file: str = None,
    caller: str = None,
):
    """! General print functionality that traces back the caller.
    @param msg (str) message to print
    @param msg_type (str, optional) message type. Defaults to "INFO".
    @param flush (bool, optional) sure that any output is buffered and go
        to the destination. Defaults to True.
    @param file (str, optional) file where the function is. Defaults to None.
        If none it inspects the stack trace to get the name.
    @param caller (str, optional) Caller of the function. Defaults to None.
        If none it inspects the stack trace to get the name.
    """
    if not flush:
        return

    file = (
        os.path.splitext(os.path.basename(inspect.stack()[1][1]))[0].upper()
        if file is None
        else file
    )
    caller = inspect.stack()[1][3].upper() if caller is None else caller
    _str = "[{}][{}][{}]: {}".format(bcolors.LOG[msg_type][1], file, caller, msg)

    print(bcolors.LOG[msg_type][0] + _str + bcolors.ENDC, flush=True)


def print_text_list(
    img,
    tex_list: list,
    color: tuple = (0, 0, 255),
    orig: tuple = (10, 25),
    fontScale: float = 0.7,
    y_jump: int = 30,
):

    """!
    Print a text list on image in desending order
    @param img 'cv2.math' image to draw components
    @param tex_list 'list' list with text to print/draw
    @param color 'tuple' bgr opencv color of text
    @param orig 'tuple' origin to start draw components
    @param fontScale 'float' text font scale
    @param y_jump 'int' jump or space between lines
    """

    for idx, text in enumerate(tex_list):

        cv2.putText(
            img=img,
            text=text,
            org=(orig[0], int(orig[1] + y_jump * idx)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=fontScale,
            color=(0, 0, 0),
            thickness=3,
            lineType=cv2.LINE_AA,
        )
        cv2.putText(
            img=img,
            text=text,
            org=(orig[0], int(orig[1] + y_jump * idx)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=fontScale,
            color=color,
            thickness=1,
            lineType=cv2.LINE_AA,
        )


def print_text_list2(
    img, data_list: list, orig=(10, 25), fontScale: float = 0.7, y_jump: int = 30
):

    """!
    Print a text list on image in desending order
    @param img 'cv2.math' image to draw components
    @param data_list 'list' list with text to print/draw
    @param orig 'tuple' origin to start draw components
    @param fontScale 'float' text font scale
    @param y_jump 'int' jump or space between lines
    """

    for idx, data in enumerate(reversed(data_list)):

        cv2.putText(
            img=img,
            text=data[0],
            org=(orig[0], int(orig[1] + y_jump * idx)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=fontScale,
            color=(0, 0, 0),
            thickness=3,
            lineType=cv2.LINE_AA,
        )
        cv2.putText(
            img=img,
            text=data[0],
            org=(orig[0], int(orig[1] + y_jump * idx)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=fontScale,
            color=data[1],
            thickness=1,
            lineType=cv2.LINE_AA,
        )


def dotline(
    src: np.ndarray, p1: tuple, p2: tuple, color: tuple, thickness: int, Dl: int
):
    """!
    Draws a doted line on input image
    @param src `cv2.mat` source image
    @param p1 `tuple` line's first point
    @param p2  `tuple` line's second point
    @param color `tuple` lines' color RGB [B, G, R] [int]
    @param thickness `int` lines' thickness
    @param Dl `int` distance in pixels between every point
    @return src `cv2.mat` image with doted line drawn
    """
    # Get a number of intermediate points
    segments = discrete_contour((p1, p2), Dl)

    for segment in segments:  # Draw doted line
        cv2.circle(img=src, center=segment, radius=thickness, color=color, thickness=-1)

    return src


def overlay_image(
    l_img: np.ndarray, s_img: np.ndarray, pos: tuple, transparency: float
):
    """!
    Overlay 's_img on' top of 'l_img' at the position specified by
    pos and blend using 'alpha_mask' and 'transparency'.
    @param l_img `cv2.mat` inferior image to overlay superior image
    @param s_img `cv2.mat` superior image to overlay
    @param pos  `tuple`  position to overlay superior image [pix, pix]
    @param transparency `float` transparency in overlayed image
    @return l_img `cv2.mat` original image with s_img overlayed
    """
    # Get superior image dimensions
    _, _, s_img_channels = s_img.shape

    if s_img_channels == 3 and transparency != 1:
        s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2BGRA)
        s_img_channels = 4

    # Take 3rd channel of 'img_overlay' image to get shapes
    img_overlay = s_img[:, :, 0:4]

    # cords assignation to overlay image
    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(l_img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(l_img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], l_img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], l_img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return l_img

    if s_img_channels == 4:
        # Get alphas channel
        alpha_mask = (s_img[:, :, 3] / 255.0) * transparency
        alpha_s = alpha_mask[y1o:y2o, x1o:x2o]
        alpha_l = 1.0 - alpha_s

        # Do the overlay with alpha channel
        for c in range(0, l_img.shape[2]):
            l_img[y1:y2, x1:x2, c] = (
                alpha_s * img_overlay[y1o:y2o, x1o:x2o, c]
                + alpha_l * l_img[y1:y2, x1:x2, c]
            )

    elif s_img_channels < 4:
        # Do the overlay with no alpha channel
        if l_img.shape[2] == s_img.shape[2]:
            l_img[y1:y2, x1:x2] = s_img[y1o:y2o, x1o:x2o]
        else:
            printlog(
                msg="Error: to overlay images should have the same color channels",
                msg_type="ERROR",
            )
            return l_img

    # Return results
    return l_img


def insert_image(
    original_image: np.ndarray,
    inserted_image: np.ndarray,
    new_width: int,
    new_height: int,
    position: int = "uc",
    line_width: int = 2,
    border_color: tuple = (255, 255, 255),
    interpolation=cv2.INTER_NEAREST,
):

    """!
    Inserts an image "inserted_image" over input image "original_image"
    @param original_image `cv2.math` background image
    @param inserted_image `cv2.math` overlayed image
    @param new_width  `int` new width for overlayed image
    @param new_height `int` new height for overlayed image
    @param positon `string` corner to overlay image. It can be defined
            as upper left: ul, upper right: ur, lower left: ll and lower right: lr
    @param line_width `int` frame line width
    @param border_color `list` [B,G,R] color to draw a frame in output image
    @param interpolation `string` interpolation flag to resize images
    """

    # Overlay image to upper left side
    height, width, _ = original_image.shape
    if position == "ul":
        original_image[0:new_height:, 0:new_width, :] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image, (0, 0), (new_width, new_height), border_color, line_width
        )

    # Overlay image to upper right side
    elif position == "ur":
        original_image[0:new_height:, -new_width:, :] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image,
            (width - new_width, 0),
            (width, new_height),
            border_color,
            line_width,
        )

    # Overlay image to upper center side
    elif position == "uc":
        original_image[
            0:new_height:,
            int(width * 0.5 - new_width * 0.5) : int(width * 0.5 + new_width * 0.5),
            :,
        ] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image,
            (int(width * 0.5 - new_width * 0.5), 0),
            (int(width * 0.5 + new_width * 0.5), new_height),
            border_color,
            line_width,
        )

    # Overlay image to lower left side
    elif position == "ll":
        original_image[-new_height:, 0:new_width, :] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image,
            (0, height - new_height),
            (new_width, height),
            border_color,
            line_width,
        )

    # Overlay image to lower right side
    elif position == "lr":
        original_image[-new_height:, -new_width:, :] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image,
            (width - new_width, height - new_height),
            (width, height),
            border_color,
            line_width,
        )

    # Overlay image to center right side
    elif position == "cr":
        original_image[
            int(original_image.shape[0] * 0.5 - new_height * 0.5) : int(
                original_image.shape[0] * 0.5 - new_height * 0.5
            )
            + new_height,
            -new_width:,
            :,
        ] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image,
            (
                width - new_width,
                int(original_image.shape[0] * 0.5 - new_height * 0.5),
            ),
            (width, int(original_image.shape[0] * 0.5 + new_height * 0.5)),
            border_color,
            line_width,
        )

    # Overlay image to center left side
    elif position == "cl":
        original_image[
            int(original_image.shape[0] * 0.5 - new_height * 0.5) : int(
                original_image.shape[0] * 0.5 - new_height * 0.5
            )
            + new_height,
            0:new_width,
            :,
        ] = cv2.resize(
            inserted_image, (new_width, new_height), interpolation=interpolation
        )
        cv2.rectangle(
            original_image,
            (
                0,
                int(original_image.shape[0] * 0.5 - new_height * 0.5),
            ),
            (new_width, int(original_image.shape[0] * 0.5 + new_height * 0.5)),
            border_color,
            line_width,
        )


# =============================================================================
# MATH/GEOMETRY OPERATIONS - MATH/GEOMETRY OPERATIONS - MATH/GEOMETRY OPERATION


def flat_matrix_for_service(numpy_array):

    """!
    Flat numpy matrix in vector
    @param numpy_array: `np.array` matrix to flat
    @return `list` vector of matrix flatten
    """
    numpy_array = np.array(numpy_array)

    rows = len(numpy_array)
    cols = len(numpy_array[0])
    nelem = rows * cols
    elems = numpy_array.reshape(1, nelem)[0]

    return list(np.append([float(rows), float(cols)], elems))


def matrix_from_flat(list_vector):
    """!
    Reshape a list vector to matrix numpy array
    @param list_vector `list` list to convert to numpy array (matrix)
    @return `numpy.array` matrix of list reshaped
    """

    rows = list_vector[0]
    cols = list_vector[1]

    return np.array(list_vector[2:]).reshape(rows, cols)


def line_intersection(line1, line2):
    """!
    Returns the instersection coordinate between two lines
    @param line1 `tuple` line 1 to calculate intersection coordinate
    @param line2 `tuple` line 2 to calculate intersection coordinate
    @return `tuple` intersection cord between line 1 and line 2
    """

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return int(round(x)), int(round(y))


def discrete_contour(contour, Dl):
    """!
    Takes contour points to get a number of intermediate points
    @param contour `List` contour or list of points to get intermediate points
    @param Dl `int` distance to get a point by segment
    @return new_contour `List` new contour with intermediate points
    """

    # If contour has less of two points is not valid for operations
    if len(contour) < 2:
        printlog(msg="No valid segment", msg_type="ERROR")
        return contour

    # New contour variable
    new_contour = []

    # Iterate through all contour points
    for idx, cordinate in enumerate(contour):

        # Select next contour for operation
        if not idx == len(contour) - 1:
            next_cordinate = contour[idx + 1]
        else:
            next_cordinate = contour[0]

        # Calculate length of segment
        segment_lenth = math.sqrt(
            (next_cordinate[0] - cordinate[0]) ** 2
            + (next_cordinate[1] - cordinate[1]) ** 2
        )

        divitions = segment_lenth / Dl  # Number of new point for current segment
        dy = next_cordinate[1] - cordinate[1]  # Segment's height
        dx = next_cordinate[0] - cordinate[0]  # Segment's width

        if not divitions:
            ddy = 0  # Dy value to sum in Y axis
            ddx = 0  # Dx value to sum in X axis
        else:
            ddy = dy / divitions  # Dy value to sum in Y axis
            ddx = dx / divitions  # Dx value to sum in X axis

        # get new intermediate points in segments
        for idx in range(0, int(divitions)):
            new_contour.append(
                (int(cordinate[0] + (ddx * idx)), int(cordinate[1] + (ddy * idx)))
            )

    # Return new contour with intermediate points
    return new_contour


# =============================================================================
