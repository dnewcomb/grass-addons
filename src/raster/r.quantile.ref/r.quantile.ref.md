## DESCRIPTION

*r.quantile.ref* computes for each pixel the quantile ranking of the
input value against the reference maps: values of 0, 0.5 and 1.0
respectively indicate that the input value corresponds with the minimum,
median or maximum of the reference values. A value of -1 is assigned if
the input value is smaller than the minimum and a value of 2 is assigned
if the input value is larger than the maximum.

*r.quantile.ref* can be regarded as the inverse of *r.series
method=quantile*: while *r.series* calculates the value for a given
quantile, *r.quantile.ref* calculates the quantile for a given value.
This is useful to compare e.g. current environmental conditions to a
time series of historical environmental conditions.

## EXAMPLE

Create some reference rasters:

```sh
r.mapcalc "ref1 = 1"
r.mapcalc "ref2 = 2"
r.mapcalc "ref3 = 3"
r.mapcalc "ref4 = 5"
r.mapcalc "ref5 = 5"
r.mapcalc "ref6 = 5"
```

Create a test raster with cell value 4.5:

```sh
r.mapcalc "test = 4.5"
```

Get the quantile of the test raster for the reference maps:

```sh
r.quantile.ref input=test reference=ref1,ref2,ref3,ref4,ref5,ref6 output=test_quant
```

The quantile corresponding to the value 4.5 is 0.55. Create a test
raster with cell value 5:

```sh
r.mapcalc "test = 5"
```

Get the quantile of the test raster for the reference maps:

```sh
r.quantile.ref input=test reference=ref1,ref2,ref3,ref4,ref5,ref6 output=test_quant
```

The quantile corresponding to the value 5 is 0.8.

## SEE ALSO

*[r.quantile](https://grass.osgeo.org/grass-stable/manuals/r.quantile.html),
[r.series](https://grass.osgeo.org/grass-stable/manuals/r.series.html)*

## AUTHOR

Markus Metz
