#  ----------------------------------------------------------------------
# Clear std out
clear

#  ----------------------------------------------------------------------
# Source local enviroment variables
source "${PWD%}/dev_ws/configs/env_vars.sh"

# -----------------------------------------------------------------------
if [ "$DOWNLOAD_EXAMPLE_DATASET" == "1" ] || [ -z "$DOWNLOAD_EXAMPLE_ID" ]; then
        mkdir ${PWD%}/dev_ws/media/images
        TEMP_FILE_NAME="everyday_studio_dataset_example.zip"
        if [ -f "${PWD%}/dev_ws/media/images/${TEMP_FILE_NAME}" ];
            then
                echo "sample dataset ${TEMP_FILE_NAME} already exits"
            else
                echo "downloading dataset, please wait ..."
                gdown https://drive.google.com/uc?id=${DOWNLOAD_EXAMPLE_ID} -O "${PWD%}/dev_ws/media/images/${TEMP_FILE_NAME}"
                unzip "${PWD%}/dev_ws/media/images/${TEMP_FILE_NAME}" -d "${PWD%}/dev_ws/media/images/"
                # rm -f "${PWD%}/dev_ws/media/images/${TEMP_FILE_NAME}"
        fi
fi

# -----------------------------------------------------------------------
# create local files
FACE_PREDICTO_FILE_PATH=${PWD%}/dev_ws/configs/${PREDICTOR_NAME%}
if test -f "$FACE_PREDICTO_FILE_PATH"; then
    echo "face landmarks file $FACE_PREDICTO_FILE_PATH already exists in configs"
else
    git submodule update --init
    cp ${PWD%}/dev_ws/src/facial_features/shape_predictor_68_face_landmarks.dat $FACE_PREDICTO_FILE_PATH
    echo "face landmarks file $FACE_PREDICTO_FILE_PATH copied to configs"
fi

# -----------------------------------------------------------------------
# Run every-day studio
python3 "${PWD%}/dev_ws/src/everyday_studio/every_day_maker.py"

# -----------------------------------------------------------------------
exit 0