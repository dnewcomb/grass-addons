## DESCRIPTION

*v.what.strds.timestamp* matches points with a timestamp in the
attribute table (*timestamp\_column*) (e.g. recordings from stationary
(temperature logger, wildlife camera traps) or non-stationary sensors
(e.g GPS collars)) with Space Time Raster Datasets (STRDS) based on
point locaitions in space and time. Raster values at the specific
space-time position are written into the user-defined *column* in the
attribute table of the input vector map.

## NOTES

The SQLite DB backend does not provide specific date/datetime datatypes.
However, text columns with ISO formated date strings are supported for
the *timestamp\_column* as well.

Curretnly, *only STRDS with absolute temporal type are supported.*

## EXAMPLE

This example is based on the MODIS LST raster time series sample dataset
(mapset "modis\_lst") available for the North Carolina sample location
which can be downloaded from the [GRASS GIS
website](https://grass.osgeo.org/download/data/).

```sh
# Check time MODIS LST raster time series to sample
t.rast.list LST_Day_monthly@modis_lst

# Set computational region to first raster map of the time series
g.region -up raster=MOD11B3.A2015001.h11v05.single_LST_Day_6km \
    align=MOD11B3.A2015001.h11v05.single_LST_Day_6km

# Create sampling points map with timestamp column for sampling time
echo "cat,sampling_time,x,y
1,2015-01-12,-125870.664090128,591821.149756026
2,2015-02-01,77667.7974483332,571718.585653462
3,2015-02-27,351565.233345769,481257.047191923
4,2015-03-10,565154.976935513,375718.585653462
5,2015-04-07,366642.156422692,277718.585653462
6,2015-05-22,178180.617961154,363154.483089359
7,2015-06-12,12334.464115,395821.149756026
8,2016-03-04,112847.28462782,204846.790781667
9,2016-05-12,311360.105140641,26436.5343714103
10,2017-01-03,467154.976935513,8846.79078166676
11,2018-01-01,600334.464115,129462.175397051
12,2016-06-07,690796.002576538,262641.662576539
13,2016-08-16,685770.361550897,441051.918986795
14,2016-12-11,625462.669243205,594333.970268846" > sampling_points.txt

# Import sampling points
v.in.ascii in=sampling_points.txt out=sampling_points x=3 y=4 cat=1 \
    columns='cat int, sampling_time date, x double precision, y double precision' \
     separator="," skip=1

# Assign LST values to sampling points at time of sampling
v.what.strds.timestamp input=sampling_points \
    timestamp_column=sampling_time column=lst_at_sampling_time \
    strds=LST_Day_monthly@modis_lst

# Check result
v.db.select sampling_points
cat|sampling_time|x|y|lst_at_sampling_time
1|2015-01-12|-125870.664090128|591821.149756026|13811
2|2015-02-01|77667.7974483332|571718.585653462|13486
3|2015-02-27|351565.233345769|481257.047191923|13793
4|2015-03-10|565154.976935513|375718.585653462|14355
5|2015-04-07|366642.156422692|277718.585653462|14565
6|2015-05-22|178180.617961154|363154.483089359|14864
7|2015-06-12|12334.464115|395821.149756026|15091
8|2016-03-04|112847.28462782|204846.790781667|14641
9|2016-05-12|311360.105140641|26436.5343714103|14982
10|2017-01-03|467154.976935513|8846.79078166676|
11|2018-01-01|600334.464115|129462.175397051|
12|2016-06-07|690796.002576538|262641.662576539|15052
13|2016-08-16|685770.361550897|441051.918986795|15052
14|2016-12-11|625462.669243205|594333.970268846|13920

# Check result for point with category 5
r.what -n map=MOD11B3.A2015091.h11v05.single_LST_Day_6km@modis_lst \
    coordinates=366642.156422692,277718.585653462

# add extra column for LST in degree Celsius
v.db.addcolumn map=sampling_points column="lst_celsius double precision"
# rescale original MODIS LST to degree Celsius
v.db.update map=sampling_points column="lst_celsius" query_column="lst_at_sampling_time * 0.02 - 273.15"
v.db.select sampling_points
```

## SEE ALSO

*[v.what.rast](https://grass.osgeo.org/grass-stable/manuals/v.what.rast.html),
[v.what.strds](https://grass.osgeo.org/grass-stable/manuals/v.what.strds.html),
[r.connectivity.corridors](https://grass.osgeo.org/grass-stable/manuals/t.rast.what.html)*

## AUTHOR

Stefan Blumentrath, Norwegian Institute for Nature Research (NINA)  
Written for the 2018 [IRSAE](https://irsae.no) GRASS GIS course at
Studenterhytta, Oslo
