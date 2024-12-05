#!/bin/bash
# get data to new log file
DATE_LOG=$(date +"%Y_%m_%d")
DATE_I=$(date +"%d/%m/%Y %H:%M")
echo "${DATE_I}" > ./generate_base_raster_${DATE_LOG}.log
echo "==============================" >> ./generate_base_raster_${DATE_LOG}.log
./generate_base_raster.sh >> ./generate_base_raster_${DATE_LOG}.log 2>&1
echo "==============================" >> ./generate_base_raster_${DATE_LOG}.log
DATE_F=$(date +"%d/%m/%Y %H:%M")
echo "${DATE_F}" >> ./generate_base_raster_${DATE_LOG}.log