#!/bin/bash

# Change this to your specific directory if needed
DIRECTORY='/workspace/dev_ws/media/images/2024'

# New folder for the converted images
NEW_FOLDER="$DIRECTORY/ConvertedImages"


# Create the new directory if it doesn't exist
mkdir -p "$NEW_FOLDER"

# Loop through all HEIC files in the directory and convert them to PNG
for HEIC in "$DIRECTORY"/*.HEIC; do
    if [ -f "$HEIC" ]; then
        echo "Converting $HEIC to PNG..."
        # Save the converted file in the new folder
        heif-convert "$HEIC" "$NEW_FOLDER/$(basename "${HEIC%.HEIC}.png")"
    fi
done

# Loop through all JPG files in the directory and convert them to PNG
for JPG in "$DIRECTORY"/*.JPG; do
    if [ -f "$JPG" ]; then
        echo "Converting $JPG to PNG..."
        # Save the converted file in the new folder
        heif-convert "$JPG" "$NEW_FOLDER/$(basename "${JPG%.JPG}.png")"
    fi
done