## DESCRIPTION

Image segmentation is the process of grouping similar pixels into unique
segments. Boundary and region based algorithms are described in the
literature, currently a region growing and merging algorithm is
implemented. Each grouping (usually refered to as objects or segments)
found during the segmentation process is given a unique ID and is a
collection of contiguous pixels meeting some criteria. (Note the
contrast with image classification, where continuity and spatial
characteristics are not important, but rather only the spectral
similarity.) The results can be useful on their own, or used as a
preprocessing step for image classification. The segmentation
preprocessing step can reduce noise and speed up the classification.

## NOTES

### Region Growing and Merging

This segmentation algorithm sequentially examines all current segments
in the map. The similarity between the current segment and each of its
neighbors is calculated according to the given distance formula.
Segments will be merged if they meet a number of criteria, including: 1.
The pair is mutually most similar to each other (the similarity distance
will be smaller then all other neighbors), and 2. The similarity must be
lower then the input threshold. All segments are checked once per pass.
The process is repeated until no merges are made during a complete pass.

### Similarity and Threshold

The similarity between segments and unmerged pixels is used to determine
which are merged. The Euclidean version uses the radiometric distance
between the two segments and also the shape characteristics. The
Manhatten calculations currently only uses only the radiometric distance
between the two segments, but eventually shape characteristics will be
included as well. NOTE: Closer/smaller distances mean a lower value for
the similarity indicates a closer match, with a similarity score of zero
for identical pixels.

During normal processing, merges are only allowed when the similarity
between two segments is lower then the calculated threshold value.
During the final pass, however, if a minimum segment size of 2 or larger
is given with the *minsize* parameter, segments with a smaller pixel
count will be merged with their most similar neighbor even if the
similarity is greater then the threshold.

Unless the *-w* flag for weighted data is used, the threshold should be
set by the user between 0 and 1.0. A threshold of 0 would allow only
identical valued pixels to be merged, while a threshold of 1 would allow
everything to be merged.

The threshold will be multiplied by the number of rasters included in
the image group. This will allow the same threshold to achieve similar
segmentation results when the number of rasters in the image group
varies.

The -t flag will estimate the threshold, it is calculated at 3% of the
range of data in the imagery group. Initial empirical tests indicate
threshold values of 1% to 5% are reasonable places to start.

#### Calculation Formulas

Both Euclidean and Manhattan distances use the normal definition,
considering each raster in the image group as a dimension. Furthermore,
the Euclidean calculation also takes into account the shape
characteristics of the segments. The normal distances are multiplied by
the input radiometric weight. Next an additional contribution is added:
(1-radioweight) \* {smoothness \* smoothness weight + compactness \*
(1-smoothness weight)}, where compactness = the Perimeter Length / sqrt(
Area ) and smoothness = Perimeter Length / the Bounding Box. The
perimeter length is estimated as the number of pixel sides the segment
has.

### Seeds

The seeds map can be used to provide either seed pixels (random or
selected points from which to start the segmentation process) or seed
segments (results of previous segmentations or classifications). The
different approaches are automatically detected by the program: any
pixels that have identical seed values and are contiguous will be lumped
into a single segment ID.

It is expected that the *minsize* will be set to 1 if a seed map is
used, but the program will allow other values to be used. If both
options are used, the final iteration that ignores the threshold also
will ignore the seed map and force merges for all pixels (not just
segments that have grown/merged from the seeds).

### Maximum number of starting segments

For the region growing algorithm without starting seeds, each pixel is
sequentially numbered. The current limit with CELL storage is 2 billion
starting segment ID's. If the initial map has a larger number of
non-null pixels, there are two workarounds:

1\. Use starting seed pixels. (Maximum 2 billion pixels can be labeled
with positive integers.)

2\. Use starting seed segments. (By initial classification or other
methods.)

### Boundary Constraints

Boundary constraints limit the adjacency of pixels and segments. Each
unique value present in the *bounds* raster are considered as a MASK.
Thus no segments in the final segmentated map will cross a boundary,
even if their spectral data is very similar.

### Minimum Segment Size

To reduce the salt and pepper affect, a *minsize* greater than 1 will
add one additional pass to the processing. During the final pass, the
threshold is ignored for any segments smaller then the set size, thus
forcing very small segments to merge with their most similar neighbor.

## EXAMPLES

This example uses the ortho photograph included in the NC Sample
Dataset. Set up an imagery group:  

```sh
i.group group=ortho_group input=ortho_2001_t792_1m@PERMANENT
```

Because the segmentation process is computationally expensive, start
with a small processing area to confirm if the segmentation results meet
your requirements. Some manual adjustment of the threshold may be
required.  

```sh
g.region raster=ortho_2001_t792_1m@PERMANENT n=220400 s=220200 e=639000 w=638800
```

Try out a first threshold and check the results.  

```sh
i.segment -w -l group=ortho_group output=ortho_segs threshold=4 \
          method=region_growing
```

From a visual inspection, it seems this results in oversegmentation.
Increasing the threshold:  

```sh
i.segment -w -l --overwrite group=ortho_group output=ortho_segs \
          threshold=10 method=region_growing
```

This looks better. There is some noise in the image, lets next force all
segments smaller then 5 pixels to be merged into their most similar
neighbor (even if they are less similar then required by our
threshold):  

```sh
i.segment -w -l --overwrite group=ortho_group output=ortho_segs \
          threshold=10 method=region_growing minsize=5
```

Each of these segmentation steps took less then 1 minute on a decent
machine. Now that we are satisfied with the settings, we'll process the
entire image:

```sh
g.region raster=ortho_2001_t792_1m@PERMANENT

i.segment -w -l --overwrite group=ortho_group output=ortho_segs \
          threshold=10 method=region_growing minsize=5 endt=5000
```

Processing the entire ortho image (over 9 million pixels) took about a
day.

## TODO

### Functionality

- Further testing of the shape characteristics (smoothness,
    compactness), if it looks good it should be added to the Manhatten
    option. **in progress**
- Malahanobis distance for the similarity calculation.

### Use of Segmentation Results

- Improve the optional output from this module, or better yet, add a
    module for *i.segment.metrics*.
- Providing updates to i.maxlik to ensure the segmentation output can
    be used as input for the existing classification functionality.
- Integration/workflow for *r.fuzzy*.

### Speed

- See create\_isegs.c

### Memory

- User input for how much RAM can be used.
- Check input map type(s), currently storing in DCELL sized SEG file,
    could reduce this dynamically depending on input map time. (Could
    only reduce to FCELL, since will be storing mean we can't use CELL.
    Might not be worth the added code complexity.)

## BUGS

If the seeds map is used to give starting seed segments, the segments
are renumbered starting from 1. There is a chance a segment could be
renumbered to a seed value that has not yet been processed. If they
happen to be adjacent, they would be merged. (Possible fixes: a. use a
processing flag to make sure the pixels hasn't been previously used, or
b. use negative segment ID's as a placeholder and negate all values
after the seed map has been processed.)

## REFERENCES

This project was first developed during GSoC 2012. Project
documentation, Image Segmentation references, and other information is
at the [project
wiki](https://grasswiki.osgeo.org/wiki/GRASS_GSoC_2012_Image_Segmentation).

Information about [classification in GRASS
GIS](https://grasswiki.osgeo.org/wiki/Image_classification) is also
available on the wiki.

## SEE ALSO

*[i.group](https://grass.osgeo.org/grass-stable/manuals/i.group.html),
[i.maxlik](https://grass.osgeo.org/grass-stable/manuals/i.maxlik.html),
[r.fuzzy](r.fuzzy),
[i.smap](https://grass.osgeo.org/grass-stable/manuals/i.smap.html),
[r.seg](r.seg.md) (Addon)*

## AUTHORS

Eric Momsen - North Dakota State University

GSoC mentor: Markus Metz
