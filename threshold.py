import gdal,ogr, osr
import glob
import os
import numpy as np 

fname=glob.iglob("TIFF/*")
dam_wkt="POLYGON((120.5807 23.1582,120.5291 23.0818,120.5519 23.0707,120.5778 23.1337,120.5879 23.1527,120.5807 23.1582))"

type_mapping = {gdal.GDT_Byte: ogr.OFTInteger,
    gdal.GDT_UInt16: ogr.OFTInteger,
    gdal.GDT_Int16: ogr.OFTInteger,
    gdal.GDT_UInt32: ogr.OFTInteger,
    gdal.GDT_Int32: ogr.OFTInteger,
    gdal.GDT_Float32: ogr.OFTReal,
    gdal.GDT_Float64: ogr.OFTReal,
    gdal.GDT_CInt16: ogr.OFTInteger,
    gdal.GDT_CInt32: ogr.OFTInteger,
    gdal.GDT_CFloat32: ogr.OFTReal,
    gdal.GDT_CFloat64: ogr.OFTReal}
    
for gt in fname:
	date=os.path.split(gt)[1].split(".")[0]
	# Read original image TIFF
	img=gdal.Open(gt)
	mndwi=img.GetRasterBand(1).ReadAsArray()
	threshold=np.std(mndwi)
	mn2=mndwi.copy()
	mn2[mndwi<threshold*1.2]=-1
	mn2[mndwi>threshold*1.2]+=1


	# SAVE TO NEW RASTER mask/
	drv=gdal.GetDriverByName("GTiff")
	[col, row]=mn2.shape
	outtiff=gt.replace(".tif","_mak.tif").replace("TIFF","mask")
	if "mask" not in os.listdir(): os.mkdir("mask")
	# Create(self,path, row, col, bands, dtype)	
	img2=drv.Create(outtiff, row, col,1, gdal.GDT_Float32)
	img2.SetGeoTransform(img.GetGeoTransform())
	img2.SetProjection(img.GetProjection())
	img2.GetRasterBand(1).WriteArray(mn2)
	img2.GetRasterBand(1).SetNoDataValue(-9999)

	img.FlushCache()
	del img, mn2, mndwi
	srcband=img2.GetRasterBand(1)


	# polygonize
	shp_path="vector\\{0}\\{0}.shp".format(date)
	if "vector" not in os.listdir(): os.mkdir("vector")
	if date not in os.listdir("vector"): os.mkdir("vector\\"+date)

	drv2  = ogr.GetDriverByName("ESRI Shapefile")
	dst_ds = drv2.CreateDataSource(shp_path)
	srs = osr.SpatialReference(wkt=img2.GetProjection())
	dst_layername="Shape"
	dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)

	raster_field = ogr.FieldDefn('id', type_mapping[srcband.DataType])
	dst_layer.CreateField(raster_field)
	gdal.Polygonize(srcband, srcband, dst_layer, 0, [], callback=None)

	img2.FlushCache()
	del img2, srcband

	
	filt = ogr.CreateGeometryFromWkt(dam_wkt)

	WGS84=osr.SpatialReference()
	WGS84.ImportFromEPSG(4326)
	tf=osr.CoordinateTransformation(WGS84,srs)

	filt.Transform(tf)
	asum=[]
	for i in dst_layer:
		area=i.GetGeometryRef().GetArea()
		if i.GetGeometryRef().Intersect(filt) and area>5000:
			asum.append(area)
		else:
			dst_layer.DeleteFeature(i.GetFID())
	print("Water Area of",date,":",sum(asum))

	del dst_ds
