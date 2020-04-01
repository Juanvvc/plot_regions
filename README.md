# plot_regions

This is a tool for regional scenery creators of FlightGear.

*plot_regions* parses XML files and plots the areas declared in these files on a world map. The intended input is "XML files in directory `$FG_ROOT/Materials/regions`".

Under the GPLv3. See LICENSE.

# Dependencies

- matplotlib
- geopandas

On Debian/Ubuntu, they can be installed from the repositories or pip. Run any of these commands:

```
> apt-get install python3-matplotlib python3-geopandas
> pip3 install --user matplotlib geopandas
```

# Usage

```
usage: plot_regions.py [-h] [-v] [-o OUTPUT] [-s WORLDSHAPE] [-w WORLDCOLOR]
                       [-f FACECOLOR] [-a ALPHA] [--single]
                       [--material MATERIAL] [--legend]
                       [--edgecolor EDGECOLOR] [--height HEIGHT]
                       [--width WIDTH] [--boundaries BOUNDARIES]
                       input

Plot FlightGear's regional materials on a world map

positional arguments:
  input                 The input XML file, or directory containing a
                        materials.xml file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose
  -o OUTPUT, --output OUTPUT
                        The output directory
  -s WORLDSHAPE, --worldshape WORLDSHAPE
                        The SHP of the world
  -w WORLDCOLOR, --worldcolor WORLDCOLOR
                        The color of the world shape
  -f FACECOLOR, --facecolor FACECOLOR
                        The color of the region shape
  -a ALPHA, --alpha ALPHA
                        The alpha value of the region shape
  --single              Save all files a single PNG file. Ignored if input is
                        not a directory.
  --material MATERIAL   If single mode, proccess only files containing this
                        material
  --legend              If single mode, show legend
  --edgecolor EDGECOLOR
                        The color of the edges of the subregion
  --height HEIGHT       The height of the figure, in inches (DPI=100)
  --width WIDTH         The width of the figure, in inches (DPI=100)
  --boundaries BOUNDARIES
                        Boundaries [minlon,maxlon,minlat,maxlat]
```

# Examples

Single file, output to `regions/indonesia.xml.png`:

```
python3 plot_regions.py -o regions $FG_ROOT/Materials/regions/indonesia.xml
```

![Indonesia](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/regions/indonesia.xml.png)

All regions, multiple files, output to directory `regions`:

```
python3 plot_regions.py -o regions $FG_ROOT/Materials/regions
```

Results: <https://github.com/Juanvvc/plot_regions/tree/master/output>

All regions, single file, output to `regions.png`:

```
python3 plot_regions.py --single $FG_ROOT/Materials/regions
```

![All regions](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/regions.png)

All regions, single file, with legend, output to `examples/regions.png`:

```
python3 plot_regions.py --legend --output examples --single $FG_ROOT/Materials/regions
```

![All regions, legend](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/examples/regions.png)

All regions defining IrrCrop, output to `materials/IrrCrop.png`, with legend:

```
python3 plot_regions.py --single --legend --material IrrCrop --output materials -a 1 --edgecolor gray $FG_ROOT/Materials/regions
```

![IrrCrop](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/materials/IrrCrop.png)


All regions defining IrrCrop, output to './IrrCrop.png', order as priorities:

```
python3 plot_regions.py --single --legend --material IrrCrop --output materials -a 1 --edgecolor gray --boundaries '[-30, 45, 30, 70]' $FG_ROOT/Materials/regions
```

![IrrCrop Europe](https://raw.githubusercontent.com/Juanvvc/plot_regions/master/examples/IrrCrop.png)


# World map Shape

The default world map shape was made with Natural Earth. Free vector and raster map
data @ naturalearthdata.com.

<https://www.naturalearthdata.com/downloads/110m-physical-vectors/>

All versions of Natural Earth raster + vector map data found on this website
are in the public domain. You may use the maps in any manner, including
modifying the content and design, electronic dissemination, and offset
printing. The primary authors, Tom Patterson and Nathaniel Vaughn Kelso, and
all other contributors renounce all financial claim to the maps and invites you
to use them for personal, educational, and commercial purposes.

No permission is needed to use Natural Earth. Crediting the authors is
unnecessary.
