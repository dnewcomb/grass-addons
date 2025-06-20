## DESCRIPTION

The *r.vif* module computes the variance inflation factor
([VIF](https://en.wikipedia.org/wiki/Variance_inflation_factor)) \[1\]
and the square root of the VIF. The VIF quantifies how much the variance
(the square of the estimate's standard deviation) of an estimated
regression coefficient is increased because of
[multi-collinearity](https://en.wikipedia.org/wiki/Multicollinearity).
The square root of VIF is a measure of how much larger the standard
error is, compared with what it would be if that variable were
uncorrelated with the other predictor variables in the model.

By default, the VIF is calculated for each variable. If the user sets a
VIF threshold value (maxvif) a stepwise variable selection procedure
\[2\] is used whereby after computing the VIF for each explanatory
variable, the variable with the highest VIF is removed. Next, the VIF
values are computed again for the reduced set of variables. This will be
repeated till the VIF is smaller than maxvif. This can thus be used to
select a sub-set of variables for e.g., multiple regression analysis.

The user can optionally select one or more variables to be retained in
the stepwise selection. For example, let's assume the user selects the
variable *bio\_5* to be retained. If in any step this variable has the
highest VIF, the variable with the next highest VIF will be removed
instead (see the examples).

The user can set the 'v' flag to only print the finally selected
variables to the standard output (console). Note that this only works
when the stepwise selection procedure is invoked, i.e., when the maxvif
is set. This option makes it easier to use the output of r.vif in
another function directly (see example).

## NOTES

To compute the vif all data layers are read in as a numpy array
(non-data cells are ignored). When input layers are large or there are
many input layers, memory usage may become problematic. In such cases
the user may opt to sample raster values for random locations and use
that to compute the vif. The quantity of random locations to be
generated either can be defined as a positive integer, or as a
percentage of the raster map layer's cells (see
[r.random](https://grass.osgeo.org/grass-stable/manuals/r.random.html)
for details).

When using a random sub-set of raster cells as input, the user has the
option to specifies the random seed used to generate the cells. The
alternatively is to set the -s flag. In that case a radnom seed will be
used. This yields a non-deterministic result, i.e., vif values may vary
between runs. If the sub-set is too small it may even lead to
differences in variables selected when running the step-wise procedure.
Special care should be taken when many of the equations are undetermined
(the value of vif is shown as *Inf*).

As an alternative, the user can set the *f* flag to evoke the
'low-memory option'. This will use the
[r.regression.multi](r.regression.multi) function in the background to
compute R<sup>2</sup>, the most memory demanding part of the
computation. With this option, the addon can handle much larger data
sets. The disadvantage is that it runs much slower.

## EXAMPLES

The following examples are based on the nc\_climate\_spm\_2000\_2012
sample data set which you can download from [GRASS GIS sample data
download page](https://grass.osgeo.org/download/data/). This data set
contains monthly rainfall and temperature data for the years 2000 -
2012. In the examples below, the monthly data of 2000 is used. The
analyses are run on a smaller region, set below, to reduce the run time.

```sh
g.region n=226000 s=168500 w=229500 e=298500
```

### Example 1

Run VIF, setting the maximum VIF at 10. The function will print the VIF
computed at each step to the console. The same will also be written to a
text file.

```sh
MAPS=`g.list type=raster pattern=*2011*precip sep=,`
r.vif maps=$MAPS file=results1.csv maxvif=10
```

Below the results are shown (here only the first and last part of the
output is shown to save space):

```text
VIF round 1
--------------------------------------
variable            vif  sqrtvif
2011_01_precip    65.03     8.06
2011_02_precip    29.10     5.39
2011_03_precip    40.20     6.34
2011_04_precip    13.12     3.62
2011_05_precip     6.81     2.61

...
...

VIF round 7
--------------------------------------
variable            vif  sqrtvif
2011_01_precip     4.25     2.06
2011_04_precip     5.22     2.29
2011_05_precip     4.86     2.20
2011_06_precip     7.13     2.67
2011_07_precip     7.58     2.75
2011_08_precip     3.32     1.82

selected variables are:
--------------------------------------
2011_01_precip, 2011_04_precip, 2011_05_precip, 2011_06_precip, 2011_07_precip, 2011_08_precip

Statistics are written to results.csv
```

The same results are (optionally) written to a comma delimited file
(csv). It contains variables and the corresponding vif and sqrt(vif) for
each round in the stepwise variable selection. The column 'removed'
gives the variable that was removed in the previous round.

![image-alt](r_vif_example1.png)

### Example 2

Run the same VIF analysis as above, but this time tell the function to
retain the variable 2011\_02\_precip. Only the last few lines of the
results are shown below. As you can see, a different set of variables is
selected, which includes the variable '2011\_02\_precip'.

```sh
MAPS=`g.list type=raster pattern=*2011*precip sep=,`
r.vif maps=$MAPS maxvif=10 retain=2011_02_precip file=results2.csv
```

The output is:

```text
...
...
VIF round 6
--------------------------------------
variable            vif  sqrtvif
2011_02_precip     9.29     3.05
2011_03_precip     9.02     3.00
2011_04_precip     6.30     2.51
2011_05_precip     4.99     2.23
2011_06_precip     9.72     3.12
2011_07_precip     8.36     2.89
2011_08_precip     3.30     1.82

selected variables are:
--------------------------------------
2011_02_precip, 2011_03_precip, 2011_04_precip, 2011_05_precip, 2011_06_precip,
2011_07_precip, 2011_08_precip

Statistics are written to results2.csv

```

### Example 3

Like example 1, but without writing the results to file, and with the
's' flag set, which means only the list with finally selected variables
are printed to screen. This output can be directl parsed in a script.

```sh
MAPS=`g.list type=raster pattern=*2011*precip sep=,`
r.vif -s maps=$MAPS maxvif=10

```

The output is:

```text
2011_01_precip,2011_04_precip,2011_05_precip,2011_06_precip,2011_07_precip,
2011_08_precip
```

This output can be captured in a variable 'SELECTION', which is used as
input in *i.group* to create a group.

```sh
MAPS=`g.list type=raster pattern=*2011*precip sep=,`
SELECTION=`r.vif -s maps=$MAPS maxvif=10`
i.group group=group_example input=$SELECTION

```

This selects raster layers using the r.vif functions, and adds these
raster layers to the group 'group\_example':

```text
Adding raster map <2011_01_precip@climate_1970_2012> to group
Adding raster map <2011_04_precip@climate_1970_2012> to group
Adding raster map <2011_05_precip@climate_1970_2012> to group
Adding raster map <2011_06_precip@climate_1970_2012> to group
Adding raster map <2011_07_precip@climate_1970_2012> to group
Adding raster map <2011_08_precip@climate_1970_2012> to group

```

## Citation

Suggested citation:

van Breugel, P., Friis, I., Demissew, S., Lillesø, J.-P. B., & Kindt, R.
2015. Current and Future Fire Regimes and Their Influence on Natural
Vegetation in Ethiopia. Ecosystems. doi: 10.1007/s10021-015-9938-x.

## References

\[1\] Graham, M.H. 2003. Confronting multicollinearity in ecological
multiple regression. Ecology 84: 2809-2815.

\[2\] Craney, T.A., & Surles, J.G. 2002. Model-Dependent Variance
Inflation Factor Cutoff Values. Quality Engineering 14: 391-403.

## AUTHOR

Paulo van Breugel, paulo at ecodiv.earth
