# Water Area extraction for Sentinel image

## Requirement
1. csh
2. gdal
3. SNAP/gpt-sentinel data processor
 4. Python

### Python Package
  * osgeo (gdal, ogr, osr)

### Optional
  * Generic Mapping Tools ( for data presentation)

## Process step
1. Create "raw" folder and move satellite image into it.

2. excute main.csh
  - compute Modification of Normalized Difference Water Index (mndwi) by SNAP gpt.
  - Set the area to subset the image.
  - save figure to "process" folder.

2. Translate.csh
  - convert ENVI image format to GeoTIFF for python.
  - save figure to "TIFF" folder.

3. thrshold.py
  - setting threshold for mndwi value. (Default = 1.2*standard deviation)
  - save figure to "mask" folder.
  - polygonize and save shape file to "vector" folder
  - AreaCalculation: Need to assign rough water coverage first to calculate the water area.

4. plot.bat (GMT needed)
  1) for Windows system work.
  2) ogr2ogr convert shapefile to GMT compatible format
  3) GMT plot and save figure to "plot" folder.
  
