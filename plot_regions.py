#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import os.path
import logging
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import xml.etree.ElementTree as ET
import geopandas as gpd

# BBox = (-30, 45, 15, 60)  #< Europe

def load_subregions(region_file):
    """ Loads subregions in an XML file.

    Attrs:
        region_file: Path the the XML file to load.

    Returns:
        An array, each item is an array [lon1, lon2, lat1, lat2]

    Raises:
        ValueError if the file cannot be parsed
    """
    tree = ET.parse(region_file)
    root = tree.getroot()
    subregions = []
    for area in root.findall('area'):
        subregions.append([
            float(area.find('lon1').text), float(area.find('lon2').text),
            float(area.find('lat1').text), float(area.find('lat2').text)])
    return subregions


def plot_world_shape(worldshape='world/ne_110m_land.shp', worldcolor='silver', boundaries=None, figsize=None):
    """ Creates a plot with the world as a background.
    This method needs geopandas installed

    Attrs:
        worldshape: path to the SHP file to load. Use a low detailed shape file.
        worldcolor: color of the shape
        boundaries: [min_lon, max_lon, min_lat, max_lat]
        figsize: the figsize param for the figure

    Returns:
        A pair fig, axis
    """
    map_df = gpd.read_file(worldshape)
    fig, ax = plt.subplots(figsize=figsize)
    if boundaries is not None:
        ax.set_xlim(boundaries[0], boundaries[1])
        ax.set_ylim(boundaries[2], boundaries[3])
    map_df.plot(ax=ax, facecolor=worldcolor)
    return fig, ax


def plot_subregions(regions, ax, facecolor=None, alpha=0.5):
    """ Adds an array of regions to a plot

    Attrs:
        regions: an array of subregions, as returned by load_subregions()
        ax: the axis
        facecolor: color of the shape
        alpha: the alpha value of the shape

    Returns:
        The first Rectangle in the region, if any. Useful for legends
    """
    rectangles = []
    for region in regions:
        rectangles.append(Rectangle((region[0], region[2]), region[1] - region[0], region[3] - region[2], facecolor=facecolor))
    if len(rectangles) > 0:
        ax.add_collection(PatchCollection(rectangles, facecolor=facecolor, alpha=alpha, edgecolor='None'))
        return rectangles[0]
    return


def plot_subregions_in_file(filename, ax, facecolor=None, alpha=0.5):
    """ Loads subregions from a filename and plot them.
    This method uses load_subregions and plot_subregions()

    Attrs:
        filename: load subregions from this file
        ax: the axis
        facecolor: color of the subregions
        alpha: the alpha value of the subregions

    Returns:
        The first Rectangle in the region, if any. Useful for legends
    """
    subregions = load_subregions(filename)
    return plot_subregions(subregions, ax, facecolor=facecolor, alpha=alpha)


def plot_regions_in_dir(directory, ax, alpha=0.5):
    """ Loads all xml files in a directory al plots them
    This method uses plot_sibregions_in_file()
    Each region will have a differente random color

    Attrs:
        directory: load regions from this directory
        ax: the axis
        alpha: the alpha value of the subregions

    Returns:
        A set (patches, legends)
    """
    available_files = os.listdir(directory)
    cmap = plt.cm.get_cmap('hsv', len(available_files))
    patches = []
    legends = []
    for i, filename in enumerate(available_files):
        if filename == 'materials.xml':
            continue
        try:
            first_patch = plot_subregions_in_file(os.path.join(directory, filename), ax, facecolor=cmap(i), alpha=alpha)
            if first_patch is not None:
                patches.append(first_patch)
                legends.append(filename)
        except ValueError:
            logging.warning('I cannot process region: %s', os.path.join(directory, filename))
    return patches, legends


def region_to_png(filename, outdir='.', figsize=None, facecolor=None, alpha=0.5, worldcolor=None, worldshape=None):
    """ Plots an XML region file into a PNG file """
    try:
        os.makedirs(outdir, exist_ok=True)
        outfile = os.path.join(outdir, '{}.png'.format(os.path.basename(filename)))
        logging.info('Converting %s into %s', filename, outfile)
        fig, ax = plot_world_shape(worldshape=worldshape, figsize=figsize, worldcolor=worldcolor)
        ax.set_title(os.path.basename(filename))
        if plot_subregions_in_file(filename, ax, facecolor=facecolor, alpha=alpha) is not None:
            fig.savefig(outfile, bbox_inches='tight')
        plt.close(fig)
    except Exception as exc:
        logging.warning('Cannot process %s: %s', filename, exc)


def allfiles_to_png(directory, outdir='.', figsize=None, facecolor=None, alpha=0.5, worldcolor=None, worldshape=None):
    """ Plots all XML regions in a directory into PNG files """
    for filename in os.listdir(directory):
        if filename == 'materials.xml' or filename.endswith('png'):
            continue
        region_to_png(os.path.join(directory, filename), outdir=outdir, figsize=figsize, facecolor=facecolor, alpha=0.5, worldcolor=worldcolor, worldshape=worldshape)


def directory_to_png(directory, outdir='.', figsize=None, alpha=0.5, worldcolor=None, worldshape=None):
    """ Plots all XML regions in a directory into a single PNG file """
    try:
        os.makedirs(outdir, exist_ok=True)
        outfile = os.path.join(outdir, '{}.png'.format(os.path.basename(directory)))
        logging.info('Converting %s into %s', directory, outfile)
        fig, ax = plot_world_shape(worldshape=worldshape, figsize=figsize, worldcolor=worldcolor)
        ax.set_title('Available regions'.format(directory))
        plot_regions_in_dir(directory, ax, alpha=alpha)
        fig.savefig(outfile, bbox_inches='tight')
        plt.close(fig)
    except Exception as exc:
        logging.warning('Cannot process %s: %s', filename, exc)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Plot FlightGear\'s regional materials on a world map')
    parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose', default=False)
    parser.add_argument('-o', '--output', help='The output directory', default='.')
    parser.add_argument('-s', '--worldshape', help='The SHP of the world', default='world/ne_110m_land.shp')
    parser.add_argument('-w', '--worldcolor', help='The color of the world shape', default='silver')
    parser.add_argument('-f', '--facecolor', help='The color of the region shape', default='b')
    parser.add_argument('-a', '--alpha', type=float, help='The alpha value of the region shape', default=0.5)
    parser.add_argument('--single', action='store_true', help='Save all files a single PNG file', default=False)
    parser.add_argument('--height', type=float, help='The height of the figure, in inches (DPI=100)', default=9)
    parser.add_argument('--width', type=float, help='The width of the figure, in inches (DPI=100)', default=12)
    parser.add_argument('input', help='The input XML file or directory containing XML files')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if not os.path.exists(args.input):
        logging.error('Input path "%s" does not exist', args.input)
        sys.exit(1)

    if os.path.isdir(args.input):
        if args.single:
            directory_to_png(args.input,
                outdir=args.output, figsize=[args.width, args.height],
                alpha=args.alpha,
                worldcolor=args.worldcolor, worldshape=args.worldshape)
        else:
            allfiles_to_png(args.input,
                outdir=args.output, figsize=[args.width, args.height],
                facecolor=args.facecolor, alpha=args.alpha,
                worldcolor=args.worldcolor, worldshape=args.worldshape)
    else:
        region_to_png(args.input,
            outdir=args.output, figsize=[args.width, args.height],
            facecolor=args.facecolor, alpha=args.alpha,
            worldcolor=args.worldcolor, worldshape=args.worldshape)
