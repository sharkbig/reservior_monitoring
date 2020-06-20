#!/bin/csh
# Batch GDAL tranlate ENVI file to GTiff
# Image mask (Thresholding)
# Batch GDAL Polygonize

set img=`ls process/*/mnwdi.img`

if ( ! -d TIFF )  mkdir TIFF

foreach fp ($img)
  set dt=`echo $fp | awk -F/ '{print $( NF -1 )}' | awk -F_ '{print $3}'  | cut -c 1-8`
  set tifname="TIFF/$dt.tif"
  echo "$tifname creating ..."
  gdal_translate -of GTiff $fp $tifname

end 


