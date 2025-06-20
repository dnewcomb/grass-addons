## DESCRIPTION

*i.evapo.potrad* calculates the diurnal potential evapotranspiration
after Bastiaanssen (1995). This is converting all Net radiation from the
diurnal period into ET. It takes input maps of Albedo, surface skin
temperature, latitude, day of year, single-way transmissivity and takes
input value of the density of fresh water. The "-r" flag permits output
map of Diurnal net radiation to use in r.eb.eta. The "-b" flag permits a
generic longwave balance calculation from surface emissivity, Air
Temperature and a value of apparent atmospheric emissivity. The "-d"
flag is a slope/aspect correction, not really tested, reports and tests
are most welcome.

## NOTES

## TODO

Slope/aspect correction to be screened and tested by somebody in the
known.

## SEE ALSO

*[r.sun](https://grass.osgeo.org/grass-stable/manuals/r.sun.html),
[i.albedo](https://grass.osgeo.org/grass-stable/manuals/i.albedo.html),
[i.eb.eta](https://grass.osgeo.org/grass-stable/manuals/i.eb.eta.html)*

## REFERENCES

- Bastiaanssen, W.G.M., 1995. Regionalization of surface flux
    densities and moisture indicators in composite terrain; a remote
    sensing approach under clear skies in mediterranean climates. PhD
    thesis, Wageningen Agricultural Univ., The Netherland, 271 pp.
    ([PDF](https://edepot.wur.nl/206553))
- Chemin, Y., 2012. A Distributed Benchmarking Framework for Actual ET
    Models, in: Irmak, A. (Ed.), Evapotranspiration - Remote Sensing and
    Modeling. InTech.
    ([PDF](https://www.intechopen.com/books/evapotranspiration-remote-sensing-and-modeling/a-distributed-benchmarking-framework-for-actual-et-models),
    [DOI: 10.5772/23571](https://doi.org/10.5772/23571))

## AUTHOR

Yann Chemin, International Rice Research Institute, The Philippines
