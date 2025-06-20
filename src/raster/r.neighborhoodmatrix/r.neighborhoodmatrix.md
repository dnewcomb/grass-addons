## DESCRIPTION

*r.neighborhoodmatrix* identifies all adjacency relations between
objects (aka segments or clumps identified by identical integer cell
values of adjacent pixels) in a raster map and exports these as a 2xn
matrix where n is the number of neighborhood relations with each
relation listed in both directions (i.e. if a is neighbor of b, the list
will contain a,b and b,a). If a path to an output file is specified, the
matrix will be written to that file, otherwise it will be sent to
standard output.

Neighborhood relations are determined pixel by pixel, and by default
only pixels that share a common pixel boundary are considered neighbors.
When the *-d* flag is set pixels sharing a common corner (i.e. diagonal
neighbors) are also taken into account.

When the *-l* flag is set, the module additionally indicates the length
of the common border between two neighbors in number of pixels. As this
length is not clearly defined for diagonal neighbors, the *-l* flag
cannot be used in combination with the *-d* flag.

The *-c* flag currently adds column headers. Please note that **this
flag's meaning will be inversed when GRASS 8 comes out** in order to
harmonize its behaviour with that in other modules.

## NOTES

As neighborhood length is measured in pixels, this length is not in
proportion to length in map units if the location is a lat-long
location, or if the resolution is not the same in East-West and in
North-South direction (rectangular pixels).

The module respects the region settings, so if the raster map is outside
the current computational region, the resulting list of neighbors will
be empty.

## TODO

- Add flag to only output half matrix with each relation only shown
    once.
- Measure neighbordhood length in map units, not only pixels

## EXAMPLE

Start by making sure the input map is of type CELL:

```sh
r.mapcalc "bc_int = int(boundary_county_500m)"
```

Send the neighborhood matrix of the counties in the boundary\_county map
of the North Carolina dataset to standard output:

```sh
r.neighborhoodmatrix in=bc_int sep=comma
```

Idem, but also calculating neighborhood length, sending the output to a
file:

```sh
r.neighborhoodmatrix -l n=bc_int sep=comma output=county_neighbors.csv
```

## SEE ALSO

*[v.neighborhoodmatrix](v.neighborhoodmatrix.md)*

## AUTHORS

Original Python-Version: Moritz Lennert  
C-Version: Markus Metz
