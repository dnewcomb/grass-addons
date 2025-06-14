## DESCRIPTION

r.massmov is a numerical model that allows users to simulate the
expansion (runout) and deposition of mass movements over a complex
topography by approximating the heterogeneous sliding mass to a
homogeneous one-phase fluid (following the approach proposed by Savage
and Hutter (1989) and Iverson and Denlinger (2001)). The model describes
the mass movements as a two-dimensional flux taking advantage of the
shallow water equations. This formula is derived from the general
Navier-Stokes equations under the hypothesis that the vertical
components of velocity and pressure are negligible with respect to the
horizontal components, and that the vertical pressure profile can be
considered as almost hydrostatic (Kinnmark 1985).

The required inputs can be classified in three categories based on the
information type:

- raster maps of the topography, in particular the sliding surface
    topography *elev* (digital terrain model without the sliding body),
    the initial sliding mass thickness *h\_ini* and the 'distance map'
    *fluiddist*, representing the cells distance from the collapsing
    body lower limit;
- numerical parameters for the characterization of the mass material,
    density *rho* \[kg/m3\], apparent yield stress *ystress* \[Pa\],
    Chezy roughness coefficient *chezy* \[m/s2\], dynamic viscosity
    *visco* \[Pa\*s\], basal friction angle *bfrict* \[deg\], internal
    friction angle of the sliding mass during the expansion *ifrict*
    \[deg\] and the fluid rate *fluid* \[m/s\].This last parameter
    provides information on the transaction velocity of the sliding mass
    when passes from a solid state to a fluid state; together with the
    'distance map' it allows to define the amount of mass mobilized as a
    function of time. It is worth noting that depending on the selected
    rheological law different sets of parameters are mandatory;
- control parameters to stop the simulation (like maximum time step
    number *timesteps* and/or automatic stopping criterion parameters
    *stop\_thres* and *step\_thres*) and to set the number of processors
    for parallel computing (*threads*). If the parallel computing is
    activated, and unless of different settings, the program runs using
    all the available processors.

The model outputs a series of flux velocity map (*v*) and deposit depth
raster map (*h*) at different time step according to the set deltatime
parameter; additionally the module outputs two raster maps representing
the maximum thickness (*h\_max*) and velocity (*v\_max*) registered
during the simulation.

## NOTES

The generation of the model input maps, in case the simulation refer to
en existing collapse and pre and post event DTM is available, can be
performed taking advantage of the GRASS modules; in particular:

- the sliding surface can be calculated by subtracting the collapsing
    body from the pre-event DTM (r.mapcalc)
- the collapsing body thickness can evaluated by considering the
    negative differences between the post and pre-event DTM multiplied
    for the cosine of the slope (r.mapcalc and r.slope.aspect)
- the distance map from the landslide toe can be obtained by applying
    the r.grow.distance module to the rasterized limits of the landslide

## DIAGNOSTICS

The module has been tested in several cases (see references), but up to
now most of the simulations was done using a Voellmy rheology thus other
rheology laws should be better investigated.

## REFERENCES

Begueria S, Van Asch T W J, Malet J P and Grondahl S 2009 A GIS based
numerical model for simulating the kinematics of mud and debris flows
over complex terrain. Nat Hazards Earth Syst Sci, 9, 1897-1909.

Iverson R M and Denlinger R P 2001 Flow of variably fluidized granular
masses across threedimensional terrain: 1, Coulomb mixture theory.
Journal of Geophysical Research 106:537-52

Kinnmark I P E 1985 The shallow water equations: Formulation, analysis
and application. In Brebia C A and Orszag S A (eds) Lecture Notes in
Engineering 15. Berlin, Springer-Verlag:1-187

Molinari M, Cannata M, Begueria S and Ambrosi C 2012 GIS-based
Calibration of MassMov2D. Transactions in GIS, 2012, 16(2):215-231

Savage S B and Hutter K 1989 The motion of a finite mass of granular
material down a rough incline. Journal of Fluid Mechanics 199:177-215

## SEE ALSO

[r.grow.distance](https://grass.osgeo.org/grass-stable/manuals/r.grow.distance.html)  
[r.slope.aspect](https://grass.osgeo.org/grass-stable/manuals/r.slope.aspect.html)  
[r.mapcalc](https://grass.osgeo.org/grass-stable/manuals/r.mapcalc.html)  

## AUTHORS

*Original version of program:*  
Santiago Begueria

*The current version of the program (ported to GRASS7.0)*:  
Monia Molinari, Massimiliano Cannata, Santiago Begueria.
