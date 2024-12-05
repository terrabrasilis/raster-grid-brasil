from adjust_extent import bbox_align
import os
import sqlite3
from zipfile import ZipFile

# the gpkg file name
gpkg_name="lm_bioma_250"

# location of this file, used as default data dir
data_dir=os.path.realpath(os.path.dirname(__file__)+"/assets/")
file_path=f"{data_dir}/{gpkg_name}"

if not os.path.isfile(f"{file_path}.gpkg") and os.path.isfile(f"{file_path}.zip"):
    print("Input file is missing")
    print(f"{file_path}.gpkg")
    print("Waiting for GeoPackage file decompression in the assets directory before proceeding...")
    with ZipFile(f"{file_path}.zip","r") as zip_ref:
        zip_ref.extractall(f"{data_dir}/")

try:
    conn = None
    if not os.path.isfile(f"{file_path}.gpkg"):
        raise FileNotFoundError(f"File not found: {file_path}.gpkg")

    conn = sqlite3.connect(f"{file_path}.gpkg")

    # we need to load the spatial extension
    # depending on your OS and sqlite/spatialite version you might need to add 
    # '.so' (Linux) or '.dll' (Windows) to the extension name
    conn.enable_load_extension(True)
    conn.execute('SELECT load_extension("mod_spatialite")')

    cursor = conn.cursor()

    sql="SELECT bioma, (ST_MinX(geom) ||','|| ST_MinY(geom) ||','|| ST_MaxX(geom) ||','|| ST_MaxY(geom)) as bbox FROM lm_bioma_250"
    cursor.execute(sql)
    result = cursor.fetchall()

    for biome, bbox in result:
        print(f"biome={biome}")
        print(f"input={bbox}")
        bbox=bbox_align(bbox)
        if bbox is not None:
            print(f"output={bbox}")
        else:
            print("Failed to adjust input BBOX.")
        print("-"*100)
except Exception as exc:
        print("There is an error.")
        print(f"Detail: {exc}")
finally:
    # frees resourses
    if conn:
        conn.close()