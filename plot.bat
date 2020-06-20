@echo off
set folder=vector
set fig=plot
set dem=D:\\geology\\gridfiles\\TW_20m_WGS84.nc
set region=120.49/120.6/23.07/23.17

gmt grdcut %dem% -R%region% -Gcutdem.grd
gmt makecpt -T0/800/10 -Cdem1 >tmp.cpt


for /D %%i in (%folder%/*) do (
	echo %%i preparing ...
	ogr2ogr -f GMT -t_srs EPSG:4326 tmp.gmt %folder%/%%i/%%i.shp

	gmt begin %fig%//%%i jpg
		gmt basemap -JM15c -Ba2mf2m -R%region% -B+t"Nanhua Reservoir (Taiwan) %%i"
		gmt grdimage cutdem.grd -Ctmp.cpt -I+a300+ne0.8 
		gmt plot tmp.gmt -W1p,red -G220
	gmt end
	del tmp.gmt
	)

del tmp.cpt, cutdem.grd
pause
