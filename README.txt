requirement
	1.  csh 
	2. gdal
	3. SNAP/gpt-sentinel data processor
	4. Generic Mapping Tools ( for data presentation)

process step
1.  main.csh
  - compute Modification of Normalized Difference Water Index (mndwi) by SNAP gpt.
  - save figure to process folder.
2. translate.csh
  - convert ENVI image format to GeoTIFF for python to process the image.
  - save figure to "TIFF" folder.
3. thrshold.py
  - setting threst for mndwi value.
  - save figure to "mask" folder.
  - polygonize and save shape file to "vector"
  - AreaCalculation

==========
6. plot.bat
  - for Windows system work.
  - ogr2ogr convert shapefile to GMT compatible format
  - GMT plot.




* areashow -> no use
* presentation -> 