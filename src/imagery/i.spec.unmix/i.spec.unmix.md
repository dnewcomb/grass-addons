## DESCRIPTION

*i.spec.unmix* is used to perform Spectral Unmixing. The result is
written in percent (rounded to nearest integer).

![image-alt](mixed_pixels_spectrum.png)Concept of mixed pixels (Landsat
example)

## EXAMPLES

This example is based on the North Carolina Sample dataset.

Prior to spectral unmixing the pixel values (DN) of the Landsat scene
need to be converted to reflectance values (here: using DOS1):

```sh
# rename channels or make a copy to match i.landsat.toar's input name scheme:
g.copy raster=lsat7_2002_10,lsat7_2002.1
g.copy raster=lsat7_2002_20,lsat7_2002.2
g.copy raster=lsat7_2002_30,lsat7_2002.3
g.copy raster=lsat7_2002_40,lsat7_2002.4
g.copy raster=lsat7_2002_50,lsat7_2002.5
g.copy raster=lsat7_2002_61,lsat7_2002.61
g.copy raster=lsat7_2002_62,lsat7_2002.62
g.copy raster=lsat7_2002_70,lsat7_2002.7
g.copy raster=lsat7_2002_80,lsat7_2002.8
```

Calculation of reflectance values from DN using DOS1 (metadata obtained
from
[p016r035\_7x20020524.met.gz](https://www.grassbook.org/wp-content/uploads/ncexternal/landsat/2002/p016r035_7x20020524.met.gz)):

```sh
# set computational region to first Landsat band
g.region raster=lsat7_2002_10 -p

i.landsat.toar input=lsat7_2002. output=lsat7_2002_toar. sensor=tm7 \
  method=dos1 date=2002-05-24 sun_elevation=64.7730999 \
  product_date=2004-02-12 gain=HHHLHLHHL
```

The resulting Landsat bands are named `lsat7_2002_toar.1 ..
lsat7_2002_toar.8`. They are used as input for the next steps.

In order to obtain pure spectra ("endmembers") to be searched for during
the spectral unmixing process later on we can either obtain them from
spectral libraries ([ASTER Spectral
Library](https://speclib.jpl.nasa.gov/), [USGS Spectral
Library](https://speclab.cr.usgs.gov/spectral-lib.html), field
spectrometer, etc.) or through a PCA analysis as follows.

In order to identify pure endmembers, they are supposed to be in the
corners of the PCA feature space:

```sh
i.pca -n input=lsat7_2002_toar.1,lsat7_2002_toar.2,lsat7_2002_toar.3,lsat7_2002_toar.4,lsat7_2002_toar.5,lsat7_2002_toar.7 \
         output=pca_lsat7_2002_toar
d.mon wx0
# d.correlate or use scatterplot tool in g.gui
d.correlate map=pca_lsat7_2002_toar.1,pca_lsat7_2002_toar.2

# TODO: problem: how to obtain the unprojected coordinates for the corner pixels?
# (in 1998 the xgobi software did this nicely, check today's ggobi)
```

Next the ASCII file (e.g. called "spectrum.dat") containing six spectra
needs to be written using either spectral data from a spectral library
or from the PCA analysis.

Sample content of "spectrum.dat":

```text
# Channels: r g b i1 i2 i3
# Enter spectra linewise!
# 1. Sagebrush
# 2. Saltbush
# 3. Soil
# 4. Dry grass
#
Matrix: 4 by 6
row0:  8.87  13.14  11.71  35.85  28.26 10.54
row1: 13.59  20.12  19.61  70.66 34.82 16.35
row2: 28.26  34.82  38.27  40.1 38.27 23.7
row3: 10.54  16.35  23.7   38.98 40.1 38.98
```

Spectral unmixing step (requires input data to be collected in an
imagery group):

```sh
i.group group=lsat7_2002_toar subgroup=lsat7_2002_toar \
  input=lsat7_2002_toar.1,lsat7_2002_toar.2,lsat7_2002_toar.3,lsat7_2002_toar.4,lsat7_2002_toar.5,lsat7_2002_toar.7

i.spec.unmix group=lsat7_2002_toar matrix=sample/spectrum.dat result=lsat7_2002_unmix \
  error=lsat7_2002_unmix_err iter=lsat7_2002_unmix_iterations

# todo: reclass to 0..100%
```

## REFERENCES

- Neteler, M., 1999: Spectral Mixture Analysis von Satellitendaten zur
    Bestimmung von Bodenbedeckungsgraden im Hinblick auf die
    Erosionsmodellierung. M.Sc. thesis, University of Hannover, Germany.
- Neteler, M., D. Grasso, I. Michelazzi, L. Miori, S. Merler, and C.
    Furlanello, 2004. New image processing tools for GRASS. - In Proc.
    Free/Libre and Open Source Software for Geoinformatics: GIS-GRASS
    Users Conference, 12-14 Sep 2004, Bangkok, Thailand.
- Neteler, M., D. Grasso, I. Michelazzi, L. Miori, S. Merler, and C.
    Furlanello, 2005. An integrated toolbox for image registration,
    fusion and classification. International Journal of Geoinformatics,
    1(1), pp. 51-61.
    ([PDF](https://neteler.org/wp-content/uploads/neteler/papers/neteler2005_IJG_051-061_draft.pdf))

## SEE ALSO

- *[i.spec.sam](i.spec.sam.md)  
    *
- <http://www.research.att.com/\~andreas/xgobi/>
- <https://web.archive.org/web/20041230155448/https://www.public.iastate.edu/\~dicook/xgobi-book/xgobi.html>
- <https://lib.stat.cmu.edu/general/XGobi/>

## AUTHORS

Markus Neteler, University of Hannover, 1999

Mohammed Rashad (rashadkm gmail.com) (2012, update to GRASS 7)
