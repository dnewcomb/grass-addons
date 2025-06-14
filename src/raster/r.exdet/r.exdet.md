## DESCRIPTION

Correlative species distribution models (SDMs) often involve some degree
of projection into conditions non-analogous to those under which it has
been calibrated. This projection into areas with novel environmental
conditions is risky as it may be ecologically and statistically invalid.
However, depending on the research question it may be difficult to avoid
or indeed the objective of research to do so. An example is the
prediction of potential distribution of species under future climates.
The latter may include conditions hitherto not encountered in the area
of interest. It is important to identify such areas and to interpret
model results with care.

The *r.exdet* function allows you to identify areas with novel
conditions, following methods developed by Mesgaran et al. (2014)
\[1\]\[2\]. This includes areas where conditions fall outside the range
of values observed in the reference / calibration data set ( *NT1*: Type
1 novelty) or areas with novel combinations between the environmental
variables (*NT2*: Type 2 novelty), which Mesgaran et al. call the
multivariate combination novelty index.

The type 1 (*NT1*) similarity is similar to how the multi-environmental
similarity measure (MESS) computes novel climates \[3\]. In both cases
if a point is outside the range of a given covariate, it gets a negative
value based on its distance to the minimum/maximum of that covariate.
The difference is that the MESS is based on the most negative value
amongst these covariates. The NT1, on the other hand, is the sum of all
these distances. The NT1 thus accounts for all variables \[2\]. The
*NT1* can have infinite negative values to zero where zero indicates no
extrapolation beyond the univariate coverage of reference data.

The type 2 (*NT2*) similarity is based on the Mahalanobis distance and
is used to identify areas where conditions are within the range of
univariate variation but which exhibits novel combinations between
covariates. *NT2* can range from zero up to infinite positive values.
Values ranging from 0 to 1 indicate similarity (in terms of both
univariate range and multivariate combination), with values closer to
zero being more similar. Values larger than one are indicative of novel
combinations.\[1\]

*r.exdet* can also compute the most influential covariate ( *MIC* ). For
areas with novel conditions, this is the variable that has the lowest
*NT1* value. For areas with multivariate combination novelty, this is
the variable that yields the largest percentage reduction in the
Mahalanobis distance if dropped.

The function can be used to compare (1) conditions at two different
times (e.g., current climate conditions and climate conditions in 2085).
As input, the user needs to provide two different sets of environmental
variables, each representing conditions at different times. The function
can also be used to compare the conditions in two different areas. This
can be done in three different ways:

- The user can provide two different sets of environmental variables,
    each covering a different area.
- The user can provide a mask and a set of data layers describing the
    reference conditions. Conditions outside the area defined by the
    mask will then be compared with the conditions within the area
    defined by the mask.
- The user can provide a
    [region](https://grass.osgeo.org/grass64/manuals/g.region.html) and
    a set of data layers describing the reference conditions. Conditions
    in the region defined by the user are compared to the conditions in
    the current computational region.

Some of the options can be combined. For example, the use can set a
mask, a set of layers describing current conditions (**reference**) and
a set of layers providing future conditions (**projection**). In this
case, the future conditions in the whole region are compared to the
current conditions within the area defined by the MASK. (todo: provide
some examples)

## EXAMPLES

You can download a sample data set from
[https://www.climond.org/ExDet](https://www.climond.org/ExDet.aspx). The
sample data contains 4 clipped Bioclim variable layers for Australia and
South Africa sourced from the CliMond dataset. In this example we will
use the Australia data as reference and the South Africa data as
projected or test. In the example below I will assume you have
downloaded the data and imported it in the currently open
location/mapset (the coordinate system is latlon, EPSG 4326).

```sh
g.region raster=AusBio13
r.exdet -p reference=AusBio13@example,AusBio14,AusBio5,AusBio6 projection=SaBio13,SaBio14,SaBio5,SaBio6 output=AusSa
```

## CITATION

When using this tool, please cite the paper describing the method in
your publications or other derived products.

- Mesgaran, M.B., Cousens, R.D. and Webber, B.L. (2014) Here be
    dragons: a tool for quantifying novelty due to covariate range and
    correlation change when projecting species distribution models.
    Diversity & Distributions, 20: 1147-1159, DOI: 10.1111/ddi.12209.

If you want, in addition, to cite this tool, you can use:

- van Breugel, P. (2016) r.exdet, a GRASS GIS addon for the
    quantification of novel uni- and multi-variate environments. URL:
    <https://grass.osgeo.org/grass70/manuals/addons/r.exdet.html>

## REFERENCES

\[1\] Mesgaran, M.B., Cousens, R.D. and Webber, B.L. (2014) Here be
dragons: a tool for quantifying novelty due to covariate range and
correlation change when projecting species distribution models.
Diversity & Distributions, 20: 1147-1159, DOI: 10.1111/ddi.12209.

\[2\] ExDet: An stand alone extrapolation detection tool for the
modelling of species distributions. URL:
<https://www.climond.org/ExDet.aspx>

\[3\] Elith, J., Kearney, M. and Phillips, S. 2010. The art of modelling
range-shifting species. Methods in Ecology and Evolution 1:330-342.

## SEE ALSO

*[r.mess](r.mess.md)*

## AUTHOR

Paulo van Breugel, paulo at ecodiv.earth
