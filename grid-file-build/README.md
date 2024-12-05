## Grid file build

This tool allows you to create a reference grid of Brazil, in GeoTiff file format, using the fixed upper left corner as the reference origin, and the lower right corner of BBOX Brazil.

 > upper left corner = "-73.9831821589999521 5.2695808330000347"

 > lower right corner = "-28.847732158999946 -33.75117916699997"

 > BBOX = {upper_left_xmin} {upper_left_ymax} {lower_right_xmax} {lower_right_ymin}

For the resolution value, we adopted the default value of 0.00009 decimal degrees, ~10 meters.

Other important metadata informations of the output file is:

| name | value |
|------|-------|
| CRS | EPSG:4674 (SIRGAS 2000) |
| Number of bands | 1 |
| Data type | Byte |
| No data value | 255 |
| Pixel value | 255 |
| Data compression | LZW |

The output file name is defined within the "generate_base_raster.sh" script as "grid_brasil_no_data.tif"

### Environment to run

The script is Linux/Bash compatible and depends on osgeo/gdal.

We recommend the docker environment to make the procedure easier.

The first option is to use the "run-grid-file-build.sh" script which has a docker command including the name of the image used in the testing phase.

The other way is install the GDAL, with gdal_create, in your system.
```sh
# GDAL version
gdal_create --version
GDAL 3.6.3, released 2023/03/07
```

In this case, you may adjust the location path where the script will write the output file.

## References

https://gdal.org/en/stable/programs/gdal_create.html