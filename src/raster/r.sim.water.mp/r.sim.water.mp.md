## DESCRIPTION

*r.sim.water.mp* is a landscape scale simulation model of overland flow
designed for spatially variable terrain, soil, cover and rainfall excess
conditions. A 2D shallow water flow is described by the bivariate form
of Saint Venant equations. The numerical solution is based on the
concept of duality between the field and particle representation of the
modeled quantity. Green's function Monte Carlo method, used to solve the
equation, provides robustness necessary for spatially variable
conditions and high resolutions (Mitas and Mitasova 1998). The key
inputs of the model include elevation (*elevation* raster map), flow
gradient vector given by first-order partial derivatives of elevation
field (*dx* and *dy* raster maps), rainfall excess rate (*rain* raster
map or *rain\_value* single value) and a surface roughness coefficient
given by Manning's n (*man* raster map or *man\_value* single value).
Partial derivatives raster maps can be computed along with interpolation
of a DEM using the -d option in
[v.surf.rst](https://grass.osgeo.org/grass-stable/manuals/v.surf.rst.html)
module. If elevation raster map is already provided, partial derivatives
can be computed using
[r.slope.aspect](https://grass.osgeo.org/grass-stable/manuals/r.slope.aspect.html)
module. Partial derivatives are used to determine the direction and
magnitude of water flow velocity. To include a predefined direction of
flow, map algebra can be used to replace terrain-derived partial
derivatives with pre-defined partial derivatives in selected grid cells
such as man-made channels, ditches or culverts. Equations (2) and (3)
from [this
report](http://fatra.cnr.ncsu.edu/~hmitaso/gmslab/reports/cerl99/rep99.html)
can be used to compute partial derivates of the predefined flow using
its direction given by aspect and slope.

The module automatically converts horizontal distances from feet to
metric system using database/projection information. Rainfall excess is
defined as rainfall intensity - infiltration rate and should be provided
in \[mm/hr\]. Rainfall intensities are usually available from
meteorological stations. Infiltration rate depends on soil properties
and land cover. It varies in space and time. For saturated soil and
steady-state water flow it can be estimated using saturated hydraulic
conductivity rates based on field measurements or using reference values
which can be found in literature. Optionally, user can provide an
overland flow infiltration rate map *infil* or a single value
*infil\_value* in \[mm/hr\] that control the rate of infiltration for
the already flowing water, effectively reducing the flow depth and
discharge. Overland flow can be further controlled by permeable check
dams or similar type of structures, the user can provide a map of these
structures and their permeability ratio in the map *flow\_control* that
defines the probability of particles to pass through the structure (the
values will be 0-1).

Output includes a water depth raster map *depth* in \[m\], and a water
discharge raster map *discharge* in \[m3/s\]. Error of the numerical
solution can be analyzed using the *error* raster map (the resulting
water depth is an average, and err is its RMSE). The output vector
points map *output\_walkers* can be used to analyze and visualize
spatial distribution of walkers at different simulation times (note that
the resulting water depth is based on the density of these walkers). The
spatial distribution of numerical error associated with path sampling
solution can be analysed using the output error raster file \[m\]. This
error is a function of the number of particles used in the simulation
and can be reduced by increasing the number of walkers given by
parameter *nwalkers*. Duration of simulation is controlled by the
*niterations* parameter. The default value is 10 minutes, reaching the
steady-state may require much longer time, depending on the time step,
complexity of terrain, land cover and size of the area. Output walker,
water depth and discharge maps can be saved during simulation using the
time series flag *-t* and *output\_step* parameter defining the time
step in minutes for writing output files. Files are saved with a suffix
representing time since the start of simulation in minutes (e.g.
wdepth.05, wdepth.10). Monitoring of water depth at specific points is
supported. A vector map with observation points and a path to a logfile
must be provided. For each point in the vector map which is located in
the computational region the water depth is logged each time step in the
logfile. The logfile is organized as a table. A single header identifies
the category number of the logged vector points. In case of invalid
water depth data the value -1 is used.

Overland flow is routed based on partial derivatives of elevation field
or other landscape features influencing water flow. Simulation equations
include a diffusion term (*diffusion\_coeff* parameter) which enables
water flow to overcome elevation depressions or obstacles when water
depth exceeds a threshold water depth value (*hmax)*, given in \[m\].
When it is reached, diffusion term increases as given by *halpha* and
advection term (direction of flow) is given as "prevailing" direction of
flow computed as average of flow directions from the previous *hbeta*
number of grid cells.

## NOTES

A 2D shallow water flow is described by the bivariate form of Saint
Venant equations (e.g., Julien et al., 1995). The continuity of water
flow relation is coupled with the momentum conservation equation and for
a shallow water overland flow, the hydraulic radius is approximated by
the normal flow depth. The system of equations is closed using the
Manning's relation. Model assumes that the flow is close to the
kinematic wave approximation, but we include a diffusion-like term to
incorporate the impact of diffusive wave effects. Such an incorporation
of diffusion in the water flow simulation is not new and a similar term
has been obtained in derivations of diffusion-advection equations for
overland flow, e.g., by Lettenmeier and Wood, (1992). In our
reformulation, we simplify the diffusion coefficient to a constant and
we use a modified diffusion term. The diffusion constant which we have
used is rather small (approximately one order of magnitude smaller than
the reciprocal Manning's coefficient) and therefore the resulting flow
is close to the kinematic regime. However, the diffusion term improves
the kinematic solution, by overcoming small shallow pits common in
digital elevation models (DEM) and by smoothing out the flow over slope
discontinuities or abrupt changes in Manning's coefficient (e.g., due to
a road, or other anthropogenic changes in elevations or cover).

**Green's function stochastic method of solution.**  
The Saint Venant equations are solved by a stochastic method called
Monte Carlo (very similar to Monte Carlo methods in computational fluid
dynamics or to quantum Monte Carlo approaches for solving the
Schrodinger equation (Schmidt and Ceperley, 1992, Hammond et al., 1994;
Mitas, 1996)). It is assumed that these equations are a representation
of stochastic processes with diffusion and drift components
(Fokker-Planck equations).

The Monte Carlo technique has several unique advantages which are
becoming even more important due to new developments in computer
technology. Perhaps one of the most significant Monte Carlo properties
is robustness which enables us to solve the equations for complex cases,
such as discontinuities in the coefficients of differential operators
(in our case, abrupt slope or cover changes, etc). Also, rough solutions
can be estimated rather quickly, which allows us to carry out
preliminary quantitative studies or to rapidly extract qualitative
trends by parameter scans. In addition, the stochastic methods are
tailored to the new generation of computers as they provide scalability
from a single workstation to large parallel machines due to the
independence of sampling points. Therefore, the methods are useful both
for everyday exploratory work using a desktop computer and for large,
cutting-edge applications using high performance computing.

## EXAMPLE

Spearfish region:

```sh
g.region raster=elevation.10m -p
r.slope.aspect elevation=elevation.10m dx=elev_dx dy=elev_dy

# synthetic maps
r.mapcalc "rain    = if(elevation.10m, 5.0, null())"
r.mapcalc "manning = if(elevation.10m, 0.05, null())"
r.mapcalc "infilt  = if(elevation.10m, 0.0, null())"

# simulate
r.sim.water elevation=elevation.10m dx=elev_dx dy=elev_dy \
            rain=rain man=manning infil=infilt \
            nwalkers=5000000 depth=depth
```

![image-alt](r_sim_water.png)  
*Water depth map in the Spearfish (SD) area*

## ERROR MESSAGES

If the module fails with

```text
ERROR: nwalk (7000001) > maxw (7000000)!
```

then a lower *nwalkers* parameter value has to be selected.

## SEE ALSO

*[v.surf.rst](https://grass.osgeo.org/grass-stable/manuals/v.surf.rst.html),
[r.slope.aspect](https://grass.osgeo.org/grass-stable/manuals/r.slope.aspect.html),
[r.sim.sediment](https://grass.osgeo.org/grass-stable/manuals/r.sim.sediment.html)*

## AUTHOR

Helena Mitasova, Lubos Mitas  
North Carolina State University  
*<hmitaso@unity.ncsu.edu>*

Jaroslav Hofierka  
GeoModel, s.r.o. Bratislava, Slovakia  
*[hofierka@geomodel.sk](mailto:hofi@geomodel.sk)*

Chris Thaxton  
North Carolina State University  
*<csthaxto@unity.ncsu.edu>*

## REFERENCES

- Mitasova, H., Thaxton, C., Hofierka, J., McLaughlin, R., Moore, A.,
    Mitas L., 2004, [Path sampling method for modeling overland water
    flow, sediment transport and short term terrain evolution in Open
    Source
    GIS.](http://fatra.cnr.ncsu.edu/~hmitaso/gmslab/papers/II.6.8_Mitasova_044.pdf)
    In: C.T. Miller, M.W. Farthing, V.G. Gray, G.F. Pinder eds.,
    Proceedings of the XVth International Conference on Computational
    Methods in Water Resources (CMWR XV), June 13-17 2004, Chapel Hill,
    NC, USA, Elsevier, pp. 1479-1490.
    <https://doi.org/10.1016/S0167-5648(04)80159-X>
- Mitasova H, Mitas, L., 2000, [Modeling spatial processes in
    multiscale framework: exploring duality between particles and
    fields,](http://fatra.cnr.ncsu.edu/~hmitaso/gmslab/gisc00/duality.html)
    plenary talk at GIScience2000 conference, Savannah, GA.
- Mitas, L., and Mitasova, H., 1998, Distributed soil erosion
    simulation for effective erosion prevention. Water Resources
    Research, 34(3), 505-516.
- Mitasova, H., Mitas, L., 2001, [Multiscale soil erosion simulations
    for land use
    management,](http://fatra.cnr.ncsu.edu/~hmitaso/gmslab/papers/LLEmiterev1.pdf)
    In: Landscape erosion and landscape evolution modeling, Harmon R.
    and Doe W. eds., Kluwer Academic/Plenum Publishers, pp. 321-347.
- Hofierka, J, Mitasova, H., Mitas, L., 2002. GRASS and modeling
    landscape processes using duality between particles and fields.
    Proceedings of the Open source GIS - GRASS users conference 2002 -
    Trento, Italy, 11-13 September 2002.
    [PDF](http://fatra.cnr.ncsu.edu/~hmitaso/gmslab/papers/Mitasova_Helena_2.pdf),
    [(archived
    PDF)](https://web.archive.org/web/20201022173344/https://www.ing.unitn.it/~grass/conferences/GRASS2002/proceedings/proceedings/pdfs/Mitasova_Helena_2.pdf)
- Hofierka, J., Knutova, M., 2015, Simulating aspects of a flash flood
    using the Monte Carlo method and GRASS GIS: a case study of the Malá
    Svinka Basin (Slovakia), Open Geosciences. Volume 7, Issue 1, ISSN
    (Online) 2391-5447, DOI:
    [10.1515/geo-2015-0013](https://doi.org/10.1515/geo-2015-0013),
    April 2015
- Neteler, M. and Mitasova, H., 2008, [Open Source GIS: A GRASS GIS
    Approach. Third Edition.](https://grassbook.org/) The International
    Series in Engineering and Computer Science: Volume 773. Springer New
    York Inc, p. 406.
