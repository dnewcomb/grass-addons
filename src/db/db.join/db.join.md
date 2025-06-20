## DESCRIPTION

*db.join* joins the content of one attribute table into another
attribute table through common attributes.

## NOTES

*db.join* is a front-end to *db.execute* to allow easier usage. The
attribute table must be stored in a SQL database (SQLite, PostgreSQL,
MySQL, ODBC, ...). The DBF backend is not supported. Tables can be
imported with *db.in.ogr*.

## EXAMPLES

```sh
# join soils_legend into mysoils attribute table
db.join mysoils col=label otable=soils_legend ocol=shortname

# verification of join
db.select mysoils
cat|label|id|shortname|longname
1|Aab|||
2|Ba|2|Ba|Barnum silt loam
3|Bb|3|Bb|Barnum silt loam, channeled
4|BcB|4|BcB|Boneek silt loam, 2 to 6
5|BcC|5|BcC|Boneek silt loam, 6 to 9
...
```

## SEE ALSO

*[db.execute](https://grass.osgeo.org/grass-stable/manuals/db.execute.html),
[db.in.ogr](https://grass.osgeo.org/grass-stable/manuals/db.in.ogr.html),
[db.select](https://grass.osgeo.org/grass-stable/manuals/db.select.html),
[v.db.join](https://grass.osgeo.org/grass-stable/manuals/v.db.join.html),
[v.db.update](https://grass.osgeo.org/grass-stable/manuals/v.db.update.html)  
[GRASS SQL
interface](https://grass.osgeo.org/grass-stable/manuals/sql.html)*

## AUTHOR

Markus Neteler
