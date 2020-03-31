# plot_regions

This is a utility tool for scenery creators of FlightGear.

This tool parses and plot the regional terrains in `FGDATA/Materials/regions`

Under the GPLv3. See LICENSE.

# Dependencies

- matplotlib
- geopandas

# Usage

Single file:

```
python3 plot_regions -o output $FG_DATA/Materials/regions/europe.xml
```

![Europe](output/europe.png)

All regions, multiple files:

```
python3 plot_regions --single $FG_DATA/Materials/regions
```

Results: <>

All regions, single file:

```
python3 plot_regions --single $FG_DATA/Materials/regions
```

![Europe](output/regions.png)

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
