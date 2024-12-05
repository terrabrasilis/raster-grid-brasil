#!/bin/bash

# GDAL settings
export CHECK_DISK_FREE_SPACE=NO
export GDAL_CACHEMAX=10%
export GDAL_NUM_THREADS=ALL_CPUS

# Set the output directory (is mapped inside the container after run)
BASE_PATH_DATA="/main/storage/exported/files"
OUTPUT_FILE="${BASE_PATH_DATA}/grid_brasil_no_data.tif"

# force the EMBRAPA Upper Left corner and BBOX Brasil Lower Right corner
# {upper_left_xmin} {upper_left_ymax} {lower_right_xmax} {lower_right_ymin}
BBOX="-73.9831821589999521 5.2695808330000347 -28.847732158999946 -33.75117916699997"

# PIXEL_SIZE="0.00009 0.00009" # 10 m
# xsize = (xmax - xmin) / x_pixelsize
# int( (-28.847732158999946 - (-73.9831821589999521)) / 0.00009 )
xsize=501505
# ysize = (ymax - ymin) / y_pixelsize
# int( (5.2695808330000347 - (-33.75117916699997)) / 0.00009 )
ysize=433564

# https://gdal.org/en/stable/programs/gdal_create.html
# -a_ullr <ulx> <uly> <lrx> <lry>

gdal_create -ot Byte -bands 1 -burn 255 -a_nodata 255 -a_srs EPSG:4674 \
-a_ullr ${BBOX} -outsize ${xsize} ${ysize} -co "COMPRESS=LZW" -co "BIGTIFF=YES" ${OUTPUT_FILE}
