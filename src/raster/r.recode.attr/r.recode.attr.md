<h2>DESCRIPTION</h2>

The <em>r.recode.attr</em> plugin let you reclass/recode a raster layer
based on values specified in a csv table.The module requires the first
row of the CSV file to contain column headers. The table must include
at least two columns: The first column corresponds to the raster values
(or a subset of them). The remaining columns contain the
reclassification values, which can be either integers or floating-point
numbers.

<p>
For each column in the csv file (except the first one) new raster map
will be created, replacing the raster values corresponding to the first
column with those in the second (3rd, 4th, etc) column.

<p>
Users can define custom names for the output map(s). If only one output
name is provided and the CSV file contains more than two columns, the
module will automatically generate output names by appending the column
names to the provided base name.

<h2>EXAMPLES</h2>

The example uses the basic North Caroline dataset. You can download it
from (<a href="https://grass.osgeo.org/download/data/">here</a>).
Alternatively, you can install in directly from within GRASS using the
"Download sample project" option in the Data panel.

Inspect the categories of the <i>landuse</i> raster layer.

<p>
<div class="code">
<pre>
r.category map=landuse@PERMANENT
</pre>
</div>

<p>
Based on the categories of the <i>landuse</i> layer, create a CSV file
<i>reclass.csv</i>. This table assigns a friction value and a
suitability value to each attribute.

<p>
<div class="code">
<pre>
cat &lt;&lt;EOL &gt; reclass.csv
rasterID,friction,suitability
1,0.9,0
2,0.7,0.2
3,0.6,0.4
4,0.2,0.5
5,0.1,0.9
6,1,0
7,0.8,0
EOL
</pre>
</div>

<p>
Use the <em>r.recode.attr</em> addon to generate two new raster layers,
one for friction and another for suitability. Specify a base name for
the output maps. Ensure that the <b>separator</b> matches the delimiter
used in your CSV file.

<p>
<div class="code">
<pre>
r.recode.attr input=landuse output=map rules=reclass.csv separator=comma
</pre>
</div>

<p>
Note that the names of the two maps are constructed based on the
provided base name 'map' + name of the name of the column. Create for
both layers created above a color table.

<p>
<div class="code">
<pre>
r.colors map=map_friction color=oranges
r.colors map=map_suitability color=greens
</pre>
</div>

<p>
The original land use map and the derived friction and suitability maps are shown in the figure below.

<p>
<div style="text-align: center; margin: 10px;">
    <a href="r_recode_attr_01.png">
      <img src="r_recode_attr_01.png" width="600" height="269" border="0"
      alt="Example output maps of r.recode.attr"></a><br>
    <i>Figure 1: The A) friction and B) suitability maps,
        based on scores assigned to each land use category
        of the landuse map.
    </i>
</div>


<h2>SEE ALSO</h2>

<em>
<a href="https://grass.osgeo.org/grass-stable/manuals/r.reclass.html">r.reclass</a>,
<a href="https://grass.osgeo.org/grass-stable/manuals/r.recode.html">r.recode</a>
</em>

<h2>AUTHOR</h2>

Paulo van Breugel, <a href="https://ecodiv.earth">https://ecodiv.earth</a>, HAS green academy University of Applied Sciences, <a href="https://www.has.nl/en/research/professorships/innovative-bio-monitoring-professorship/">Innovative
Biomonitoring research group</a>, <a href="https://www.has.nl/en/research/professorships/climate-robust-landscapes-professorship/">Climate-robust
Landscapes research group</a>
