from adjust_extent import bbox_align

# the input BBOX (e.g. xmin,ymin,xmax,ymax)
input_bbox="-61.63331222199997,-18.041560999999945,-50.20914025899998,-7.348087549999946" # Mato Grosso

bbox=bbox_align(input_bbox)
if bbox is not None:
    print(f"output={bbox}")
else:
    print("Failed to adjust input BBOX.")