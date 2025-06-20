## DESCRIPTION

*r.flexure* computes how the rigid outer shell of a planet deforms
elastically in response to surface-normal loads by solving equations for
plate bending. This phenomenon is known as "flexural isostasy" and can
be useful in cases of glacier/ice-cap/ice-sheet loading, sedimentary
basin filling, mountain belt growth, volcano emplacement, sea-level
change, and other geologic processes. *r.flexure* and
[v.flexure](v.flexure.md) are the GRASS GIS interfaces to the model
[**gFlex**](https://csdms.colorado.edu/wiki/Model:GFlex). As both
*r.flexure* and [v.flexure](v.flexure.md) are interfaces to gFlex, this
must be downloaded and installed. The most recent versions of **gFlex**
are available from <https://github.com/awickert/gFlex>, and installation
instructions are available on that page via the *README.md* file.

## NOTES

The parameter **method** sets whether the solution is Finite Difference
("FD") or Superposition of Analytical Solutions ("SAS"). The Finite
difference method is typically faster for large arrays, and allows
lithospheric elastic thickness to be varied laterally, following the
solution of van Wees and Cloetingh (1994). However, it is quite
memory-intensive, so unless the user has a computer with a very large
amount of memory and quite a lot of time to wait, they should ensure
that they use a grid spacing that is appropriate to solve the problem at
hand. Flexural isostatic solutions act to smooth inputs over a given
flexural wavelength (see , so if an appropriate solution resolution is
chosen, the calculated flexural response can be interpolated to a higher
resolution without fear of aliasing.

The flexural solution is generated for the current computational region,
so be sure to check *g.region* before running the model\!

**input** is a 2-D array of loads in a GRASS raster. These are in units
of stress, and equal the density of the material times the acceleration
due to gravity times the thickness of the column. This is not affected
by what you choose for **g**, later: it is pre-calculated by the user.

**te**, written in standard text as T<sub>e</sub>, is the lithospheric
elastic thickness.

Several boundary conditions are available, and these depend on if the
solution method is finite difference (FD) or superposition of analytical
solutions (SAS). In the latter, it is assumed that there are no loads
outside of those that are explicitly listed, so the boundary conditions
are "NoOutsideLoads". As this is the implicit case, the boundary
conditions all default to this.

The finite difference boundary conditions are a bit more complicated,
but are largely self-explanatory:

- **0Displacement0Slope**  
    0-displacement-0-slope boundary condition
- **0Moment0Shear**  
    "Broken plate" boundary condition: second and third derivatives of
    vertical displacement are 0. This is like the end of a diving board.
- **0Slope0Shear**  
    First and third derivatives of vertical displacement are zero. While
    this does not lend itself so easily to physical meaning, it is
    helpful to aid in efforts to make boundary condition effects
    disappear (i.e. to emulate the NoOutsideLoads cases)
- **Mirror**  
    Load and elastic thickness structures reflected at boundary.
- **Periodic**  
    "Wrap-around" boundary condition: must be applied to both North and
    South and/or both East and West. This causes, for example, the edge
    of the eastern and western limits of the domain to act like they are
    next to each other in an infinite loop.

All of these boundary conditions may be combined in any way, with the
exception of the note for periodic boundary conditions. If one does not
want the boundary conditions to affect the solutions, it is recommended
that one places the boundaries at least one flexural wavelength away
from the load.

*r.flexure* may be run in latitude/longitude coordinates (with the
"**-l**" flag), but its grid constraint is that it can have only one
*dx* and one *dy* for the entire domain. Thus, it chooses the average
*dx* at the midpoint between the northernmost and southernmost latitudes
for which the calculations are made. This assumption can break down at
the poles, where the East–West dimension rapidly diminishes.

The [Community Surface Dynamics Modeling
System](https://csdms.colorado.edu), into which **gFlex** is integrated,
is a community-driven effort to build an open-source modeling
infrastructure for Earth-surface processes.

## SEE ALSO

*[v.flexure](v.flexure.md)*

## REFERENCES

Wickert, A. D. (2015), Open-source modular solutions for flexural
isostasy: gFlex v1.0, *Geoscientific Model Development Discussions*,
*8*(6), 4245–4292, doi:10.5194/gmdd-8-4245-2015.

Wickert, A. D., G. E. Tucker, E. W. H. Hutton, B. Yan, and S. D. Peckham
(2011), [Feedbacks between surface processes and flexural isostasy: a
motivation for coupling
models](https://csdms.colorado.edu/csdms_wiki/images/Andrew_Wickert_CSDMS_2011_annual_meeting.pdf),
in *CSDMS 2011 Meeting: Impact of time and process scales*, Student
Keynote, Boulder, CO.

van Wees, J. D., and S. Cloetingh (1994), A Finite-Difference Technique
to Incorporate Spatial Variations In Rigidity and Planar Faults Into 3-D
Models For Lithospheric Flexure, *Geophysical Journal International*,
*117*(1), 179–195,
[doi:10.1111/j.1365-246X.1994.tb03311.x](https://doi.org/10.1111/j.1365-246X.1994.tb03311.x).

## AUTHOR

Andrew D. Wickert
