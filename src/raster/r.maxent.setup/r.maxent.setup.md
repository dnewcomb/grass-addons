<h2>DESCRIPTION</h2>

The <em>r.maxent.setup</em> addon provides a helper function to
install Maxent and ensures that GRASS GIS can locate the Java
executable, a prerequisite for running Maxent.

<h3>Maxent</h3>

The <em>r.maxent.train</em> and <em>r.maxent.predict</em> modules
require the Maxent software, which can be downloaded from the <a
href="https://biodiversityinformatics.amnh.org/open_source/maxent">Maxent
website</a>. The <em>r.maxent.setup</em> installs this to the GRASS
GIS addon directory. If you want to update the Maxent.jar file, use the
<b>-u</b> flag.

<h3>Java</h3>

Maxent requires Java to be installed, and it should be accessible from
the GRASS GIS environment. You can check this by running the
<em>r.maxent.setup</em> with the <b>-j</b> flag.

<p>
On Windows, even if JAVA is installed and on the PATH, GRASS GIS may
still not be able to find it. The reason is that OSGeo4W environment
used by GRASS GIS on Windows has its own shell environment, which may
not automatically inherit the system-wide PATH or environment variables
from Windows. As a result, even if Java is correctly installed and
accessible from a regular Command Prompt or PowerShell, it might not be
visible to GRASS GIS within the OSGeo4W shell.

<p>
To enable GRASS GIS to find the path to the Java executable, you can
set the path to the executable using the <b>java</b> parameter. The
path will be written to a text file in the GRASS GIS addon directory,
which can be used by the <em>r.maxent.train</em> and
<em>r.maxent.predict</em> modules.

<p>
An arguably better but more involved way is to add the Java directory
to the OSGeo4W PATH. See the NOTES for a short 'how to'.


<h2>NOTES</h2>

Instead of using this addon to set the path to the java executable, you
can add the Java directory to the OSGeo4W PATH temporarily. Open
the Open the OSGeo4W shell and run the following:

<div class="code">
<pre>
set PATH=C:\Program Files\Java\jdk-XX.X.X\bin;%PATH%
</pre>
</div>

<p>
Replace C:\Program Files\Java\jdk-XX.X.X\bin with your Java
installation path.

To make this change persistent, you need to edit the <i>osgeo4w.bat</i>
file. This file can be found in the OSGeo4W installation folder. Locate
the file, and find the line that starts with <i>set PATH=</i>.

<p>
At the end of that line, add a semi-colun and the path to the Java
installation path. For example:

<p>
<div class="code">
<pre>
set PATH=%PATH%;C:\Program Files\Java\jdk-XX.X.X\bin;
</pre>
</div>

<p>
Replace C:\Program Files\Java\jdk-XX.X.X\bin with your Java
installation path. Save the file and restart the OSGeo4W shell. Note
that you may need administrator rightrs to edit the osgeo4w.bat file.

<h2>SEE ALSO</h2>

<ul>
<li><a href="v.maxent.train.html">v.maxent.train</a></li>
<li><a href="v.maxent.predict.html">v.maxent.predict</a></li>
</ul>

<h2>AUTHOR</h2>

<a href="https:ecodiv.earth">Paulo van Breugel</a>, <a
href="https://has.nl">HAS green academy</a>, <a
href="https://www.has.nl/en/research/professorships/innovative-bio-monitoring-professorship/">Innovative
Biomonitoring research group</a>, <a
href="https://www.has.nl/en/research/professorships/climate-robust-landscapes-professorship/">Climate-robust
Landscapes research group</a>
