## DESCRIPTION

*i.feo\_tio2* calculates the FeO or TiO2 contents from Clementine data.
Clementine UVVIS sensor has five bands, UVVIS1 = 415, UVVIS2 = 750,
UVVIS3 = 900, UVVIS4 = 950 and UVVIS5 = 1000 nm.

```text
wt%TiO2 = 3.708 arctan ((R415/R750)-y0Ti)/(R750-s0Ti) (1)

wt%FeO = -137.97 ( R750 sin(theta) + (R950/R750) cos(theta) ) + 57.46   (2)
```

with theta = 1.3885 rad, the 'average slope of the trends in the mare'
from Wilcox et al (2005). [Map-a-Planet
Explorer](https://web.archive.org/web/20161203071556/http://www.mapaplanet.org/explorer/help/index.html)
mentions this set of equations:

```c
double feolucey2000(double uvvis2, double uvvis4){
     //\cite{lucey2000lunar}
     return(17.427*(-atan2f(((uvvis4/uvvis2)-1.19)/(uvvis2-0.08)))-7.565);
}

double feolawrence2002(double uvvis2, double uvvis4){
     //\cite{lawrence2002iron}
     return(5.7*((-0.147+0.372*(-(uvvis4/uvvis2-1.22)/(uvvis2-0.04))+(-0.036)*pow((-(uvvis4/uvvis2-1.22)/(uvvis2-0.04)),2)))+2.15);
}

double feowilcox2005(double uvvis2, double uvvis4){
      //\cite{wilcox2005mapping}
      return(-137.97*((uvvis2*0.9834)+(uvvis4/uvvis2*0.1813))+57.46);
}

double omatlucey2000(double uvvis2, double uvvis4){
     //\cite{lucey2000lunar}
     return(sqrtf(pow((uvvis2-0.08),2)+pow(((uvvis4/uvvis2)-1.19),2)));
}

double omatwilcox2005(double uvvis2, double uvvis4){
     //\cite{wilcox2005mapping}
     return((uvvis2*0.1813)-((uvvis4/uvvis2)*0.9834));
}

double tio2lucey2000(double uvvis1, double uvvis2){
     //\cite{lucey2000lunar}
     return(3.708*pow((atan2f(((uvvis1/uvvis2)-0.42)/(uvvis2-0.0))),5.979));
}
```

## NOTES

Initially created for Clementine data.

## REFERENCES

(1) Lucey, P.G., Blewett, D.T., Jolliff, B.L., 2000. Lunar iron and
titanium abundance algorithms based on final processing of Clementine
ultraviolet-visible images. J. Geophys. Res. 105(E8): 20297-20305. (2)
Wilcox, B.B., Lucey, P.G., Gillis, J.J., 2005. Mapping iron in the lunar
mare: An improved approach. J. Geophys. Res. 110(E11):2156-2202. (3)
Lawrence, DJ and Feldman, WC and Elphic, RC and Little, RC and
Prettyman, TH and Maurice, S and Lucey, PG and Binder, AB, 2002. Iron
abundances on the lunar surface as measured by the Lunar Prospector
gamma-ray and neutron spectrometers. Journal of Geophysical Research:
Planets (1991--2012), 107(E12):13-1.

## AUTHOR

Yann Chemin (B.Sc. student), Birkbeck, University of London.
