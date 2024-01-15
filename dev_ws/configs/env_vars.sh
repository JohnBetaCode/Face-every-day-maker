# Please define here your enviroment variables and follow the docstrings and style

# ----------------------------------------------------------------------------------------------------------------------
export DEBUG_LEVEL=1                        # [int]: 0 - debug, 1 - info, 2 - warning, 3 - error, 4 - faltal
export PRINT_IMG_INFO=0                     # [bool]: Enable/Disable image information printing in the prompt
export MEDIA_PATH="/workspace/dev_ws/media/export" # [string]: path to media folder

# ----------------------------------------------------------------------------------------------------------------------
# FaceStudio configs
export FACE_STUDIO_BLURRING=1           # [bool]: Enable/Disable image background blurring
export FACE_STUDIO_BLURRING_THRESH=0.6  # [float]: Blurring threshold 
export FACE_STUDIO_BLURRING_RATIO=99    # [int]: Blurring ratio 
export FACE_STUDIO_GRAY=1               # [bool]: Enable/Disable gray color space

# ----------------------------------------------------------------------------------------------------------------------
# Window parameters
export WIN_NAME="every_day_studio"  # [string]: studio window name
export WIN_WIDTH=640                # [int][pixels]: studio window width
export WIN_HEIGHT=480               # [int][pixels]: studio window height
export WIN_TIME=-1                  # [int][mili-seconds]: studio window wait time, -1 wait until key

# ----------------------------------------------------------------------------------------------------------------------
# Video exporting params

export VIDEO_WIDTH=640      # [int][pixels]: width of output video & to resize images 
export VIDEO_HEIGHT=480     # [int][pixels]: height of output video & to resize images
export VIDEO_RATE=20                    # [int][pixels]: exported video rate, frames per second
export VIDEO_NAME="every_day"           # [string]: exported video name
export VIDEO_EXPORT_PATH="/workspace"   # [string]: exported video path
export VIDEO_EXPORT_VISUALS=1           # [bool]: Enable/Disable face visuals exportation
export VIDEO_EXPORT_PREVISUALIZATION=1  # [bool]: Enable/Disable export previsuzalitation
export VIDEO_EXPORT_DATE=1              # [bool]: Enable/Disable export date overlayed over final video
export AUDIO_TRACK="track_1.mp3"        # [string]: File name of audio track to use in video

# ----------------------------------------------------------------------------------------------------------------------