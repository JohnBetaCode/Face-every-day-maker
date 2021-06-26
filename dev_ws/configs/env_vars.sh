# Please define here your enviroment variables and follow the docstrings and style

export AUDIO_TRACK="track_1.mp3"                    # [string]: File name of audio track to use in video
export DEBUG_LEVEL=3                                # [int]: 0 - debug, 1 - info, 2 - warning, 3 - error, 4 - faltal

export CONFIGS_PATH="/workspace/dev_ws/configs"                 # [string]: path to configs file
export PREDICTOR_NAME="predictor_landmarks.dat"                 # [string]: file name of predictor for facial landmarks
export MEDIA_PATH="/workspace/dev_ws/media"                     # [string]: path to media folder
export DATASET_PATH="/workspace/dev_ws/media/images"            # [string]: path to media folder
export DOWNLOAD_EXAMPLE_DATASET=1                               # [bool]: Enable/Disable example dataset downloading
export DOWNLOAD_EXAMPLE_ID=1Oiq0NQUqQqk3kY8sOVHL1p0bMc1HQcSa    # [string]: sample dataset id 

export PREVISUALIZE_FACE_CORRECTION=1 # [bool]: Enable/Disable face correction pre-visualization

export WIN_NAME="every_day_studio"  # [string]: studio window name
export WIN_WIDTH=640                # [int][pixels]: studio window width
export WIN_HEIGHT=480               # [int][pixels]: studio window height
export WIN_TIME=-1                  # [int][mili-seconds]: studio window wait time, -1 wait until key

export VIDEO_WIDTH=640      # [int][pixels]: width of output video & to resize images 
export VIDEO_HEIGHT=360     # [int][pixels]: height of output video & to resize images
export VIDEO_RATE=20                            # [int][pixels]: exported video rate, frames per second
export VIDEO_NAME="every_day"                   # [string]: exported video name
export VIDEO_PATH="/workspace/dev_ws/export"    # [string]: exported video path
export VIDEO_EXPORT_GRAY=0                      # [bool]: Enable/Disable gray color exportation
export VIDEO_EXPORT_VISUALS=1                   # [bool]: Enable/Disable face visuals exportation
export VIDEO_EXPORT_PREVISUALIZATION=1          # [bool]: Enable/Disable export previsuzalitation
export VIDEO_EXPORT_DATE=0                      # [bool]: Enable/Disable export date overlayed over final video
