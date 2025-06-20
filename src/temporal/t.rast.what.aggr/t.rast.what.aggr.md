## DESCRIPTION

*t.rast.what.aggr* samples a space time raster dataset at points from a
vector map and returns aggregated values either printing them to stdout
or updating the attribute table. A single date for the aggregation can
be provided with the option *date* or alteratively, different dates for
each point in the vector map can be passed through the option
*date\_column*. Either *date* or *date\_column* must be provided. The
aggregation is done by default backwards in time starting from the date
provided and with the *granularity* set. Alternatively, the data can be
aggregated forward in time by using the *a* flag. By default, the output
is printed to stdout. To write the output into the attribute table of
the vector map, *u* flag must be set and the target column should be
created beforehand (See
[v.db.addcolumn](https://grass.osgeo.org/grass-stable/manuals/v.db.addcolumn.html)).
Alternatively, *c* flag creates the columns using the name of the space
time raster dataset (strds) and the method(s) as column name(s).

## NOTES

For *method=mode* the module requires
[scipy](https://www.scipy.org/scipylib/index.html) library to be
installed.

## EXAMPLES

Average NDVI for the previous 2 months starting from 2015-05-01 (i.e.:
date="2015-05-01") for all points in the vector map.

```sh
t.rast.what.aggr input=GR_GSOM_stations strds=ndvi_16_5600m \
 date=2015-05-01 granularity="2 months"

1|2015-05-01|4480.0
2|2015-05-01|5852.66666667
3|2015-05-01|5683.33333333
4|2015-05-01|4985.0
```

Average, minimum and maximum NDVI for the previous 2 months starting
from 2015-05-01 (i.e.: date="2015-05-01") for all points in the vector
map.

```sh
t.rast.what.aggr input=GR_GSOM_stations strds=ndvi_16_5600m \
 date=2015-05-01 granularity="2 months" method=average,minimum,maximum

1|2015-05-01|4480.0|4371.0|4545.0
2|2015-05-01|5852.66666667|5618.0|6249.0
3|2015-05-01|5683.33333333|5530.0|5955.0
4|2015-05-01|4985.0|4820.0|5169.0
```

Average NDVI for the previous 2 months, starting from different dates
for each point in the vector map (i.e.: providing date\_column).

```sh
t.rast.what.aggr input=GR_GSOM_stations strds=ndvi_16_5600m \
 granularity="2 months" date_column=fechas

1|2015-01-01|*
2|2015-02-01|5254.0
3|2015-03-01|6023.66666667
4|2015-04-01|4399.66666667
```

Minimum and maximum NDVI for the previous 2 months, starting from
different dates for each point in the vector map (i.e.: providing
date\_column).

```sh
t.rast.what.aggr input=GR_GSOM_stations strds=ndvi_16_5600m \
 date_column=fechas granularity="2 months" \
 method=minimum,maximum

1|2015-01-01|*|*
2|2015-02-01|5254.0|5254.0
3|2015-03-01|5944.0|6119.0
4|2015-04-01|3786.0|4820.0
```

Minimum and maximum NDVI for the 2 months after (i.e.: set -a flag) the
date provided in *date\_column*. Note that in this example the first
point gets populated.

```sh
t.rast.what.aggr -a input=GR_GSOM_stations date_column=fechas \
 granularity="2 months" strds=ndvi_16_5600m method=minimum,maximum

1|2015-01-01|3497.0|4280.0
2|2015-02-01|4801.0|6249.0
3|2015-03-01|5530.0|5955.0
4|2015-04-01|5169.0|6390.0
```

Minimum and maximum NDVI for the previous 2 months, starting from
different dates for each point in the vector map (i.e.: providing
date\_column) and write the output into the vector atrribute's table.

```sh
# create columns
v.db.addcolumn map=GR_GSOM_stations column="ndvi_min double precision"
v.db.addcolumn map=GR_GSOM_stations column="ndvi_max double precision"

# write the aggregated values to the attribute table
t.rast.what.aggr -u input=GR_GSOM_stations strds=ndvi_16_5600m \
 date_column=fechas granularity="2 months" columns=ndvi_min,ndvi_max \
 method=minimum,maximum

# check the result
v.db.select map=GR_GSOM_stations

cat|station|name|long|lat|fechas|ndvi_min|ndvi_max
1|GRE00105244|LAMIA|22.4|38.9|2015-01-01||
2|GRE00105246|TANAGRA|23.53|38.32|2015-02-01|5254|5254
3|GRE00105240|CHIOS|26.13|38.33|2015-03-01|5944|6119
4|GRE00105242|FLORINA|21.4|40.78|2015-04-01|3786|4820
```

Automatically create the columns and populate them with the aggregated
values.

```sh
t.rast.what.aggr -u -c input=GR_GSOM_stations date_column=fechas \
 granularity="2 months" strds=ndvi_16_5600m method=minimum,maximum

v.db.select map=GR_GSOM_stations
cat|station|name|long|lat|fechas|ndvi_mean|ndvi_max|ndvi_16_5600m_minimum|ndvi_16_5600m_maximum
1|GRE00105244|LAMIA|22.4|38.9|2015-01-01||||
2|GRE00105246|TANAGRA|23.53|38.32|2015-02-01|5254|5254|5254|5254
3|GRE00105240|CHIOS|26.13|38.33|2015-03-01|5944|6119|5944|6119
4|GRE00105242|FLORINA|21.4|40.78|2015-04-01|3786|4820|3786|4820
```

## SEE ALSO

*[r.what](https://grass.osgeo.org/grass-stable/manuals/r.what.html),
[t.rast.what](https://grass.osgeo.org/grass-stable/manuals/t.rast.what.html),
[t.rast.aggregate](https://grass.osgeo.org/grass-stable/manuals/t.rast.aggregate.html)*

[GRASS GIS Wiki: temporal data
processing](https://grasswiki.osgeo.org/wiki/Temporal_data_processing)

## AUTHORS

Luca Delucchi  
Documentation by Veronica Andreo
