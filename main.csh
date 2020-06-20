#!/bin/csh
# Process sentinel-2 mutispectral image.
# Preparaion:
#   create folder: raw/ and put all image in it

# setup
set a="raw/*.zip"
set bat="graph/batch.xml"
set out_folder="$PWD/process"
set gpt="/home/junyanchen/opt/snap/bin/gpt"

# subset 
set N="23.249"
set W="120.452"
set S="23.039"
set E="120.746"
set region="POLYGON(($W $S, $W $N, $E $N, $E $S, $W $S ))"

foreach file ($a)
  set target = `echo $file | sed "s\zip\_subset_mndwi.dim\g"`
  set outname="$out_folder/$target"
  echo outname
  cat $bat | sed "s\IN_FILE.zip\$PWD/$file\g"  |  sed "s\OUT_FILE.dim\$outname\g" | sed "s\POLYGON\$region\g"  > tmp_graph.xml

  echo ""
  echo ""
  echo ""
  echo "================================"
  echo $file
  echo "================================"
  gpt tmp_graph.xml
end

rm tmp_graph.xml
