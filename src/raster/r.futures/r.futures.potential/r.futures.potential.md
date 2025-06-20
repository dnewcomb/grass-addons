## DESCRIPTION

Module *r.futures.potential* implements POTENTIAL submodel as a part of
[FUTURES](r.futures.md) land change model. POTENTIAL is implemented
using a set of coefficients that relate a selection of site suitability
factors to the probability of a place becoming developed. This is
implemented using the parameter table in combination with maps of those
site suitability factors (mapped predictors). The coefficients are
obtained by conducting multilevel logistic regression in R with package
[lme4](https://cran.r-project.org/web/packages/lme4/index.html) where
the coefficients may vary by subregions. The best model is selected
automatically using `dredge` function from package
[MuMIn](https://cran.r-project.org/web/packages/MuMIn/index.html) (which
has numerous caveats).

Module *r.futures.potential* can run it two modes. Without the **-d**
flag, it uses all the given predictors to construct the model. With
**-d** flag, it evaluates all the different combinations of predictors
and picks the best one based on AIC.

### Format

The format of the output file is a CSV file (use option **separator** to
change default separator comma). The header contains the names of the
predictor maps and the first column contains the identifiers of the
subregions. The order of columns is important, the second column
represents intercept, the third development pressure and then the
predictors. Therefore the development pressure column must be specified
as the first column in option **columns**.

```csv
ID,Intercept,devpressure_0_5,slope,road_dens_perc,forest_smooth_perc,...
37037,-1.873,12.595,-0.0758,0.0907,-0.0223,...
37063,-2.039,12.595,-0.0758,0.0907,-0.0223,...
37069,-1.795,12.595,-0.0758,0.0907,-0.0223,...
37077,-1.264,12.595,-0.0758,0.0907,-0.0223,...
37085,-1.925,12.595,-0.0758,0.0907,-0.0223,...
...
```

## NOTES

Note that this module is designed to automate the FUTURES workflow by
brute-force selection of model, which has numerous caveats.

In case there is only one subregion, R function *glm* is used instead of
*glmer*.

## EXAMPLES

## SEE ALSO

[FUTURES](r.futures.md), *[r.futures.pga](r.futures.pga.md)*,
*[r.futures.devpressure](r.futures.devpressure.md)*,
*[r.futures.potsurface](r.futures.potsurface.md)*,
*[r.futures.demand](r.futures.demand.md)*,
*[r.futures.calib](r.futures.calib.md)*,
*[r.sample.category](r.sample.category.md)*

## REFERENCES

- Meentemeyer, R. K., Tang, W., Dorning, M. A., Vogler, J. B.,
    Cunniffe, N. J., & Shoemaker, D. A. (2013). [FUTURES: Multilevel
    Simulations of Emerging Urban-Rural Landscape Structure Using a
    Stochastic Patch-Growing
    Algorithm](https://doi.org/10.1080/00045608.2012.707591). Annals of
    the Association of American Geographers, 103(4), 785-807. DOI:
    10.1080/00045608.2012.707591
- Dorning, M. A., Koch, J., Shoemaker, D. A., & Meentemeyer, R. K.
    (2015). [Simulating urbanization scenarios reveals tradeoffs between
    conservation planning
    strategies](https://doi.org/10.1016/j.landurbplan.2014.11.011).
    Landscape and Urban Planning, 136, 28-39. DOI:
    10.1016/j.landurbplan.2014.11.011
- Petrasova, A., Petras, V., Van Berkel, D., Harmon, B. A., Mitasova,
    H., & Meentemeyer, R. K. (2016). [Open Source Approach to Urban
    Growth
    Simulation](https://isprs-archives.copernicus.org/articles/XLI-B7/953/2016/isprs-archives-XLI-B7-953-2016.pdf).
    Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci., XLI-B7,
    953-959. DOI: 10.5194/isprsarchives-XLI-B7-953-2016

## AUTHOR

Anna Petrasova, [NCSU GeoForAll](https://geospatial.ncsu.edu/geoforall/)
