#!/usr/bin/env bash

set -e

MEDIA_DIR=${1:-videos/rendered}
SCENE_NAME=${2}
FILE_NAME=${3}

echo "Cleaning Manim output..."

if [ -f "./media/videos/${FILE_NAME}/1080p60/${SCENE_NAME}.mp4" ]; then

    mv "./media/videos/${FILE_NAME}/1080p60/${SCENE_NAME}.mp4" \
       "$MEDIA_DIR/${SCENE_NAME}.mp4"
    echo "FULL_HD: $MEDIA_DIR/${SCENE_NAME}.mp4"
fi

if [ -f "./media/videos/${FILE_NAME}/1920p60/${SCENE_NAME}.mp4" ]; then
    mv "./media/videos/${FILE_NAME}/1920p60/${SCENE_NAME}.mp4" \
       "$MEDIA_DIR/${SCENE_NAME}.mp4"
    echo "SHORTS: $MEDIA_DIR/${SCENE_NAME}.mp4"
fi

rm -rf "./media"

echo "Done!"