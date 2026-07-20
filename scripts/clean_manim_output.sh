#!/usr/bin/env bash

set -e

MEDIA_DIR=${1:-videos/rendered}
SCENE_NAME=${2:-LexerAnimation}

echo "Cleaning Manim output..."

rm -rf "$MEDIA_DIR/images"
rm -rf "$MEDIA_DIR/texts"

if [ -f "$MEDIA_DIR/videos/scene/1920p60/$SCENE_NAME.mp4" ]; then
    mv "$MEDIA_DIR/videos/scene/1920p60/$SCENE_NAME.mp4" \
       "$MEDIA_DIR/$SCENE_NAME.mp4"
fi

rm -rf "$MEDIA_DIR/videos"

echo "Done: $MEDIA_DIR/$SCENE_NAME.mp4"