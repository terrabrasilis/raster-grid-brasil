#!/bin/bash
#
# Need a directory to use as a docker volume where output data is written.
# Adjust the path in VOLUME_HOST if necessary.
VOLUME_HOST=""
#
# detect the location of this script
SCRIPT_DIR=$(pwd)

if [[ "$2" != "up" && "$2" != "down" ]]; then
  echo "Use up to start OR down to stop."
  echo "------------------------------------------"
  echo "Example: ./run-grid-file-build.sh up"
else
  if [[ "${VOLUME_HOST}" = "" ]]; then
    VOLUME_HOST="${SCRIPT_DIR}/files"
    mkdir -p "${VOLUME_HOST}"
  fi;

  if [[ "$2" == "up" ]]; then
    docker run -d --name grid_file_build --rm -v ${SCRIPT_DIR}:/scripts \
    -v ${VOLUME_HOST}:/main/storage/exported/files \
    osgeo/gdal:ubuntu-small-3.6.3 bash /scripts/start.sh
  fi;
  if [[ "$2" == "down" ]]; then
    docker container stop grid_file_build
  fi;
fi;
