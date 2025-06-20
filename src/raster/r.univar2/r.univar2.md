## DESCRIPTION

*r.univar* calculates the univariate statistics of one or several raster
map(s). This includes the number of cells counted, minimum and maximum
cell values, range, arithmetic mean, population variance, standard
deviation, and coefficient of variation. Statistics are calculated
separately for every category/zone found in the **zones** input map if
given. If the **-e** extended statistics flag is given the 1st quartile,
median, 3rd quartile, and given **percentile** are calculated. If the
**-g** flag is given the results are presented in a format suitable for
use in a shell script. If the **-t** flag is given the results are
presented in tabular format with the given field separator. The table
can immediately be converted to a vector attribute table which can then
be linked to a vector, e.g. the vector that was rasterized to create the
**zones** input raster.

When multiple input maps are given to *r.univar*, the overall statistics
are calculated. This is useful for a time series of the same variable,
as well as for the case of a segmented/tiled dataset. Allowing multiple
raster maps to be specified saves the user from using a temporary raster
map for the result of *r.series* or *r.patch*.

## NOTES

As with most GRASS raster modules, *r.univar* operates on the raster
array defined by the current region settings, not the original extent
and resolution of the input map. See
*[g.region](https://grass.osgeo.org/grass-stable/manuals/g.region.html)*.

This module can use large amounts of system memory when the **-e**
extended statistics flag is used with a very large region setting. If
the region is too large the module should exit gracefully with a memory
allocation error. Basic statistics can be calculated using any size
input region.

Without a **zones** input raster, the *r.quantile* module will be
significantly more efficient for calculating percentiles with large
maps.

## EXAMPLE

Calculate the raster statistics for zones within a vector map coverage
and upload the results for mean, min and max back to the vector map:

```sh
#### set the raster region to match the map
g.region vector=fields res=10 -ap

#### create rasterized version of vector map
v.to.rast in=fields out=fields.10m use=cat type=area labelcolumn=label
r.colors fields.10m color=random

#### perform analysis
r.univar -t map=elevation.10m zones=fields.10m | \
  cut -f1,5,6,8 -d'|' > fields_stats.txt


#### populate vector DB with stats

# create working copy of vector map
g.copy vector=fields,fields_stats

# create new attribute columns to hold output
v.db.addcol map=fields_stats \
  columns='mean_elev DOUBLE PRECISION, min_elev DOUBLE PRECISION, max_elev DOUBLE PRECISION'

# create SQL command file, and execute it
sed -e '1d' fields_stats.txt | awk -F'|' \
  '{print "UPDATE fields_stats SET min_elev = "$2", max_elev = "$3", \
  mean_elev = "$4" WHERE cat = "$1";"}' \
   > fields_stats_sqlcmd.txt

db.execute input=fields_stats_sqlcmd.txt


#### view completed table
v.db.select fields_stats
```

## SEE ALSO

*[g.region](https://grass.osgeo.org/grass-stable/manuals/g.region.html),
[r3.univar](https://grass.osgeo.org/grass-stable/manuals/r3.univar.html),
[r.mode](https://grass.osgeo.org/grass-stable/manuals/r.mode.html),
[r.quantile](https://grass.osgeo.org/grass-stable/manuals/r.quantile.html),
[r.series](https://grass.osgeo.org/grass-stable/manuals/r.series.html),
[r.stats](https://grass.osgeo.org/grass-stable/manuals/r.stats.html),
[r.statistics](https://grass.osgeo.org/grass-stable/manuals/r.statistics.html),
[v.rast.stats](https://grass.osgeo.org/grass-stable/manuals/v.rast.stats.html),
[v.univar](https://grass.osgeo.org/grass-stable/manuals/v.univar.html)*

## AUTHORS

Hamish Bowman, Otago University, New Zealand  
Extended statistics by Martin Landa  
Multiple input map support by Ivan Shmakov  
Zonal loop by Markus Metz
