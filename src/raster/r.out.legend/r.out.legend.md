## DESCRIPTION

The *r.out.legend* script provides a quick way to create a smoothed
legend image for floating point raster maps (continuous values as
opposed to categories), with the dimensions and resolution required.
Optionally, a histogram can be added along side the legend by setting
the -d flag. In addition, most option for d.label are available in this
addon as well. The legend can be saved as
[PNG](https://grass.osgeo.org/grass-stable/manuals/pngdriver.html),
[PS](https://grass.osgeo.org/grass-stable/manuals/psdriver.html)
(postscript), BMP, PPM, PDF AND SVG. The latter four are supported
through the Cairo driver (see Notes). The images can be used to add a
continuous legends in maps created in e.g., QGIS composer or as part of
a Google Earth map.

## NOTES

The user is required to set the dimensions of the legend bar. This does
not include the category values and histogram. Both will thus add to the
size of the output image. The size of the output image in pixels and the
unit set by the user is given in the console (see example 1).

Note that one can use category maps as input, but *r.out.legend* will
still create a smooth legend (by setting the -f flag, see *d.legend*).

The user may create a horizontal legend by making the box wider than it
is tall. Note that for vertical legends labels are placed to the right
of the legend box. For horizontal legends the text will be places below
the legend.

The -d flag is used to display a histogram distribution along side the
legend. For vertical legends, the histogram will be placed left of the
legend; if horizontal, it will be placed above the legend bar. The
histogram is 1.75 x the width (or height if horizontal) of the legend
bar. This thus adds to the final width of the output image. Note that
the statistics are calculated on the current computational region
settings set by g.region. The default range however covers the entire
natural bounds of the input map. If the histogram appears empty, check
your region settings.

The script is a wrapper of
[d.legend](https://grass.osgeo.org/grass-stable/manuals/d.legend.html).
For detailed explanations of the different options, see the manual pages
of this functions. To find out the fonts available on your system, you
can run
[d.font](https://grass.osgeo.org/grass-stable/manuals/d.font.html)
**-l**. For a more interactive way to generate legend images, you can
also try [ps.map](ps.map).

With file type set to 'png', the png driver is used to create the image.
An alternative way to create a png image file is to set as file type
'cairo' and provide an output file name with as extension '.png'. This
will use the cairo driver to generate the png image. One advantage of
the cairo driver is that it uses anti-aliasing, which might give nicer
results (smoother lines and numbers). Compare the output for example 1
and 4.

The default resolution is 300 px/inch (ppi), except when the unit is set
to *px*, in which case the default resolution is set to 96 ppi.

If the output image is in png or jpg format, the addon will attempt to
set the print resolution of the image so that other programs, such as
Libreoffice or Word document, know the intended size of the image. It
uses the Python Imaging Library
([PIL](http://www.pythonware.com/products/pil/)) to do so. If not
installed this step will silently be skipped. However, note that the
dimensions of the image (in the user-defined unit, and based on the
user-defined image resolution) will be printed to the console.

The *range* option lets the user define the limits of the legend. Note
however that the color scale will remain faithful to the values as
defined with r.colors.

The [Cairo
driver](https://grass.osgeo.org/grass64/manuals/cairodriver.html)
generates PNG, BMP, PPM, PS, PDF or SVG images using the Cairo graphics
library. The image format is selected from the extension of the output
file. For this option to work, GRASS has to be configured with CAIRO
support (if you compile GRASS yourself, use --with-cairo when
configuring GRASS).

## EXAMPLES

The raster layers in the examples below are from the [North Carolina
sample data set](https://grass.osgeo.org/download/data/).

### Example 1

Note that because width \> height, the legend is printed horizontal,
with the labels below the legend bar.

```sh
r.out.legend raster=elevation file=r_out_legend_1.png filetype=png \
    dimensions=4,0.4 labelnum=3 fontsize=7 unit="cm" resolution=150
```

![image-alt](r_out_legend_1.png)

The dimensions (width and height) of the image are printed to the
console.

```text
----------------------------
File saved as r_out_legend_1.png
The image dimensions are:
285px wide and 49px heigh
at a resolution of 150 ppi this is:
4.826 cm x 0.8382 cm
----------------------------
```

### Example 2

Same as above, but the font is set to comic and the background color us
set to grey.

```sh
r.out.legend raster=elevation file=r_out_legend_2.png filetype=png \
    dimensions=300,20 labelnum=3 fontsize=10 unit="px" \
    font=comic bgcolor=grey
```

![image-alt](r_out_legend_2.png)

### Example 3

Like example 1, but without the raster values printed (done by setting
fontsize to 0).

```sh
r.out.legend raster=elevation file=r_out_legend_3.png filetype=png \
    dimensions=300,20 labelnum=3 fontsize=0 unit="px"
```

![image-alt](r_out_legend_3.png)

### Example 4

Like example 1, but using the cairo driver to create the png image. The
difference is that the cairo driver uses anti-aliasing.

```sh
r.out.legend raster=elevation file=r_out_legend_4.png filetype=cairo \
    dimensions=4,0.4 labelnum=3 fontsize=7 unit="cm" resolution=150
```

![image-alt](r_out_legend_4.png)

The dimensions (width and height) of the image:

```text
----------------------------
File saved as r_out_legend_4.png
The image dimensions are:
286px wide and 50px heigh
at a resolution of 150 ppi this is:
4.84293333333 cm x 0.855133333333 cm
----------------------------
```

### Example 5

Like example 4, but adding a histogram. Note that the histogram adds to
the size of the image (while the dimensions of the bar remain the same
as in the previous example).

```sh
r.out.legend raster=elevation file=r_out_legend_5.png filetype=cairo \
    dimensions=4,0.4 labelnum=3 fontsize=7 unit="cm" resolution=150 -d
```

![image-alt](r_out_legend_5.png)

The dimensions (width and height) of the image:

```text
----------------------------
File saved as r_out_legend_5.png
The image dimensions are:
286px wide and 92px heigh
at a resolution of 150 ppi this is:
4.84293333333 cm x 1.56633333333 cm
----------------------------
```

## SEE ALSO

*[d.mon](https://grass.osgeo.org/grass-stable/manuals/d.mon)*,
*[d.legend](https://grass.osgeo.org/grass-stable/manuals/d.legend)*,
*[d.font](https://grass.osgeo.org/grass-stable/manuals/d.font)*,
*[d.out.file](https://grass.osgeo.org/grass-stable/manuals/d.out.file.html)*,
*[ps.map](https://grass.osgeo.org/grass-stable/manuals/ps.map.html)*,
*[r.category.trim](r.category.trim.md)*

## AUTHOR

Paulo van Breugel, paulo at ecodiv.org
