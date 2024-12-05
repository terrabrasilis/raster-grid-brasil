from osgeo import gdal
import os
from zipfile import ZipFile


def bbox_align(bbox:str, data_dir:str=None)->str:
    """
    Used to align any input extent coordinates to the Brasil reference grid.
    We expect that:
        - input bbox* is inside the reference grid bbox;
        - input geotiff file was named as grid_brasil_no_data

    parameters:
        bbox, the input bbox, as string, to adjust. The separator character is a comma. (e.g. xmin,ymin,xmax,ymax)*;
        data_dir, the location of reference grid file;

    The output is the adjusted input bbox compatible with the expected bbox from the -te parameter to the gdal_rasterize program (gdal_rasterize -te ${BBOX} ).
    The separator character is a space (e.g. xmin ymin xmax ymax)*

    *Each coordinate value must be a floating point number in degree units compatible with the Geographic/SIRGAS2000 projection, EPSG:4674.
    """
    # location of this file, used as default data dir
    script_dir=os.path.realpath(os.path.dirname(__file__)+"/assets/")
    # use the location of this script file as default when DATA_DIR is not provided
    data_dir=script_dir if data_dir is None else data_dir
    # the geotiff file that represents the grid
    grid_name="grid_brasil_no_data"

    # test input bbox
    if not bbox:
        print("BBOX entry is missing")
        return None
    
    bbox=bbox.split(',')
    if not len(bbox)==4:
        print("BBOX input is not in the expected format: 'xmin,ymin,xmax,ymax' ")
        return None

    XMIN=float(bbox[0])
    YMIN=float(bbox[1])
    XMAX=float(bbox[2])
    YMAX=float(bbox[3])

    # input geotiff as reference grid
    file_path = f"{data_dir}/{grid_name}"
    if not os.path.isfile(f"{file_path}.tif") and os.path.isfile(f"{file_path}.zip"):
        print("Input file is missing")
        print(f"{file_path}.tif")
        print("Waiting for grid file decompression in the assets directory before proceeding...")
        with ZipFile(f"{file_path}.zip","r") as zip_ref:
            zip_ref.extractall(f"{data_dir}/")

    def adjust_x(x_value, xOrigin, pixelWidth):
        lon = float(x_value)
        col = int((lon - xOrigin) / pixelWidth)
        return xOrigin + pixelWidth * col

    def adjust_y(y_value, yOrigin, pixelHeight):
        lat = float(y_value)
        row = int((yOrigin - lat ) / pixelHeight)
        return yOrigin - pixelHeight * row
        
    try:
        if not os.path.isfile(f"{file_path}.tif"):
            raise FileNotFoundError(f"File not found: {file_path}.tif")
        
        dataset = gdal.Open(f"{file_path}.tif", gdal.GA_ReadOnly)
        transform = dataset.GetGeoTransform()

        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = -transform[5]

        upper_left_xmin=adjust_x(x_value=XMIN, xOrigin=xOrigin, pixelWidth=pixelWidth)
        upper_left_ymax=adjust_y(y_value=YMAX, yOrigin=yOrigin, pixelHeight=pixelHeight)
        lower_right_xmax=adjust_x(x_value=XMAX, xOrigin=xOrigin, pixelWidth=pixelWidth)
        lower_right_ymin=adjust_y(y_value=YMIN, yOrigin=yOrigin, pixelHeight=pixelHeight)

        return f"{upper_left_xmin} {lower_right_ymin} {lower_right_xmax} {upper_left_ymax}"

    except Exception as exc:
        print("There is an error.")
        print(f"Detail: {exc}")
    finally:
        # frees memory
        dataset = None

    return None
