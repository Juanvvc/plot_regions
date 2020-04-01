# plot_regions

This is a utility tool for scenery creators of FlightGear.

This tool parses and plot the regional terrains in `FGDATA/Materials/regions`

Under the GPLv3. See LICENSE.

# Dependencies

- matplotlib
- geopandas

# Usage

Single file, output to directory `output`:

```
python3 plot_regions.py -o output $FG_DATA/Materials/regions/indonesia.xml
```

![Indonesia](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/output/indonesia.xml.png)

All regions, multiple files, output to directory `$FG_DATA/Materials/regions`:

```
python3 plot_regions.py -o $FG_DATA/Materials/regions $FG_DATA/Materials/regions
```

Results: <https://github.com/Juanvvc/plot_regions/tree/master/output>

All regions, single file, output to `./regions.png`:

```
python3 plot_regions.py --single $FG_DATA/Materials/regions
```

![All regions](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/regions.png)

# World map Shape

Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.
<https://www.naturalearthdata.com/downloads/110m-physical-vectors/>

All versions of Natural Earth raster + vector map data found on this website
are in the public domain. You may use the maps in any manner, including
modifying the content and design, electronic dissemination, and offset
printing. The primary authors, Tom Patterson and Nathaniel Vaughn Kelso, and
all other contributors renounce all financial claim to the maps and invites you
to use them for personal, educational, and commercial purposes.

No permission is needed to use Natural Earth. Crediting the authors is
unnecessary.
