#!/bin/bash

CURRENT_TAG=$(cat image_tag.txt)
NEW_TAG=$IMAGE_TAG

if [ "$CURRENT_TAG" != "$NEW_TAG" ]; then
  echo "IMAGE_TAG has changed from $CURRENT_TAG to $NEW_TAG"
  echo $NEW_TAG > image_tag.txt
  exit 0
else
  echo "IMAGE_TAG has not changed"
  exit 1
fi