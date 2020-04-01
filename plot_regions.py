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
import random
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import xml.etree.ElementTree as ET
import geopandas as gpd

MATERIALS_FILE = 'materials.xml'   #< file including all available materials


def list_files(materials_file, material=None):
    """ Read MATERIALS_FILE and list include files.
    Optionaly, only files including a specific material are included.
    This function assumes that all region files are in the same directory that MATERIALS_FILE,
    and they only the filename is returned.    
    
    Params:
        materials_file: path to the MATERIALS_FILE file.
    
    Return:
        The available files, in priority order as FlightGear understand priority
    """
    tree = ET.parse(materials_file)
    root = tree.getroot()
    parent_directory = os.path.dirname(materials_file)
    files = []
    for region in root.findall('region'):
        region_path = region.attrib.get('include', None)
        if region_path is None:
            continue
        region_filename = os.path.basename(region_path)
        region_assumed_path = os.path.join(parent_directory, region_filename)
        if file_contains_material(region_assumed_path, material):
            files.append(region_filename)
    return files


def file_contains_material(filename, material=None):
    """ Returns True if the file contains the specific material.
    If material is None, returns True. """
    if material is None:
        return True
    tree = ET.parse(filename)
    root = tree.getroot()
    for m in root.findall('material'):
        for n in m.findall('name'):
            if n.text == material:
                return True
    return False


def load_subregions(region_file):
    """ Loads subregions in an XML file.

    Params:
        region_file: Path the XML file to load.

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


def create_figure(boundaries=None, figsize=None):
    """ Creates a matplotlib figure

    Params:
        boundaries: [min_lon, max_lon, min_lat, max_lat]
        figsize: the figsize param for the matplotlib.figure.Figure

    Returns:
        A pair (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    fig, ax = plt.subplots(figsize=figsize)
    if boundaries is not None:
        ax.set_xlim(boundaries[0], boundaries[1])
        ax.set_ylim(boundaries[2], boundaries[3])
    else:
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
    return fig, ax


def plot_world_shape(ax, worldshape='world/ne_110m_land.shp', worldcolor='silver', edgecolor=None):
    """ Creates a plot with the world as a background.

    Params:
        ax: the matplotlib.axes.Axes
        worldshape: path to the SHP file to load. Use a low detailed shape file.
        worldcolor: color of the shape
    """
    map_df = gpd.read_file(worldshape)
    map_df.plot(ax=ax, facecolor=worldcolor, edgecolor=edgecolor)


def plot_subregions(filename, ax, facecolor=None, edgecolor="None", alpha=0.5):
    """ Adds an array of regions to a plot

    Params:
        filename: load subregions from this file
        ax: the matplotlib.axes.Axes
        facecolor: color of the shape
        alpha: the alpha value of the shape

    Returns:
        The first Rectangle in the region, if any. Useful for legends
    """
    subregions = load_subregions(filename)
    rectangles = []
    for subregion in subregions:
        rectangles.append(Rectangle((subregion[0], subregion[2]), subregion[1] - subregion[0], subregion[3] - subregion[2], facecolor=facecolor))
    if len(rectangles) > 0:
        ax.add_collection(PatchCollection(rectangles, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha))
        return rectangles[0]
    return


def random_colors(number):
    """ Returns a list of random colors for matplotlib """
    cmap = plt.cm.get_cmap('hsv', number)
    colors = []
    for c in range(0, number):
        colors.append(cmap(c))
    random.shuffle(colors)
    return colors


def plot_regions(directory, ax, alpha=0.5, edgecolor="None", material=None):
    """ Loads XML files listed in MATERIALS_FILE in a directory and plots them
    This method uses plot_subregions()
    Each region will have a different random color

    Params:
        directory: load regions from this directory
        ax: the matplotlib.axes.Axes
        alpha: the alpha value of the subregions
        edgecolor: the edge color for subregions (useful if there are many regions on the same map)
        material: if not None, list only files which define this material

    Returns:
        A set (patches, legends)
    """
    available_files = list_files(os.path.join(directory, MATERIALS_FILE), material=material)
    patches = []
    legends = []
    colors = random_colors(len(available_files))
    for i, filename in enumerate(available_files):
        try:
            first_patch = plot_subregions(os.path.join(directory, filename), ax, facecolor=colors[i], edgecolor=edgecolor, alpha=alpha)
            if first_patch is not None:
                patches.append(first_patch)
                legends.append(filename)
        except ValueError:
            logging.warning('I cannot process region: %s', os.path.join(directory, filename))
    return patches, legends


def region_to_png(filename, outdir='.', figsize=None, boundaries=None, facecolor=None, edgecolor='None', alpha=0.5, worldcolor=None, worldshape=None):
    """ Plots an XML region file into a PNG file.
    
    Params:
        filename: The path to the XML file.
        outdir: save the PNG file in this directory. Output PNG will be {outdir}/{filename}.png
        figsize: the figsize param for the matplotlib.figure.Figure
        boundaries: [min_lon, max_lon, min_lat, max_lat] or None
        facecolor: color of the region
        edgecolor: color of the subregions
        alpha: alpha of the region
        worldcolor: color of the world shape
        worldshape: path to the SHP of the world
    """
    try:
        os.makedirs(outdir, exist_ok=True)
        outfile = os.path.join(outdir, '{}.png'.format(os.path.basename(filename)))
        logging.info('Converting %s into %s', filename, outfile)
        fig, ax = create_figure(figsize=figsize, boundaries=boundaries)
        plot_world_shape(ax, worldshape=worldshape, worldcolor=worldcolor)
        ax.set_title(os.path.basename(filename))
        if plot_subregions(filename, ax, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha) is not None:
            # plot the world edges on top
            plot_world_shape(ax, worldshape=worldshape, worldcolor="None", edgecolor=worldcolor)
            fig.savefig(outfile, bbox_inches='tight')        
        plt.close(fig)
    except Exception as exc:
        logging.warning('Cannot process %s: %s', filename, exc)


def directory_to_png(directory, outdir='.', figsize=None, boundaries=None, facecolor=None, edgecolor='None', alpha=0.5, worldcolor=None, worldshape=None):
    """ Plots all XML regions in a directory into PNG files.
    
    Params:
        directory: The path to directory containing a MATERIALS_FILE.
        outdir: save the PNG file in this directory. Output will be {outdir}/{region_filename}.png
        figsize: the figsize param for the matplotlib.figure.Figure
        boundaries: [min_lon, max_lon, min_lat, max_lat] or None
        facecolor: color of the region
        edgecolor: color of the subregions
        alpha: alpha of the regions
        worldcolor: color of the world shape
        worldshape: path to the SHP of the world    
    """
    for filename in list_files(os.path.join(directory, MATERIALS_FILE)):
        region_to_png(os.path.join(directory, filename), outdir=outdir, figsize=figsize, facecolor=facecolor, edgecolor=edgecolor, alpha=0.5, worldcolor=worldcolor, worldshape=worldshape)


def directory_to_single_png(directory, outdir='.', material=None, figsize=None, boundaries=None, edgecolor='None', alpha=0.5, worldcolor=None, worldshape=None, legend=False):
    """ Plots all XML regions in a directory into a single PNG file.
   
    Params:
        directory: The path to directory containing a MATERIALS_FILE.
        outdir: save the PNG file in this directory. Output will be:
            - {outdir}/{dirname}.png, if no material is defined
            - {outdir}/{material}.png, if a material is defined
        material: plot only regions including this material.
        figsize: the figsize param for the matplotlib.figure.Figure
        boundaries: [min_lon, max_lon, min_lat, max_lat] or None
        edgecolor: color of the subregions
        alpha: alpha of the regions
        worldcolor: color of the world shape
        worldshape: path to the SHP of the world
        legend: if True, include a legend
    """
    os.makedirs(outdir, exist_ok=True)
    if material is not None:
        outfile = os.path.join(outdir, '{}.png'.format(material))
    else:
        outfile = os.path.join(outdir, '{}.png'.format(os.path.basename(directory)))
    logging.info('Converting %s into %s', directory, outfile)
    fig, ax = create_figure(figsize=figsize, boundaries=boundaries)
    plot_world_shape(ax, worldshape=worldshape, worldcolor=worldcolor)
    if material is not None:
        ax.set_title('Regions defining {}'.format(material))
    else:
        ax.set_title('Available regions'.format(directory))    
    patches, legends = plot_regions(directory, ax, alpha=alpha, material=material, edgecolor=edgecolor)
    if legend:
        # two columns, to the right of the figure
        plt.legend(patches, legends, bbox_to_anchor=(1.05, 1), loc=2, ncol=2)
    # draw the outline of the world on top
    plot_world_shape(ax, worldshape=worldshape, worldcolor=(0, 0, 0, 0), edgecolor=worldcolor)
    fig.savefig(outfile, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    import argparse
    import sys
    import ast

    parser = argparse.ArgumentParser(description='Plot FlightGear\'s regional materials on a world map')
    parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose', default=False)
    parser.add_argument('-o', '--output', help='The output directory', default='.')
    parser.add_argument('-s', '--worldshape', help='The SHP of the world', default='world/ne_110m_land.shp')
    parser.add_argument('-w', '--worldcolor', help='The color of the world shape', default='silver')
    parser.add_argument('-f', '--facecolor', help='The color of the region shape', default='b')
    parser.add_argument('-a', '--alpha', type=float, help='The alpha value of the region shape', default=0.5)
    parser.add_argument('--single', action='store_true', help='Save all files a single PNG file. Ignored if input is not a directory.', default=False)
    parser.add_argument('--material', help='If single mode, proccess only files containing this material', default=None)
    parser.add_argument('--legend', action='store_true', help='If single mode, show legend', default=False)
    parser.add_argument('--edgecolor', help='The color of the edges of the subregion', default='None')
    parser.add_argument('--height', type=float, help='The height of the figure, in inches (DPI=100)', default=9)
    parser.add_argument('--width', type=float, help='The width of the figure, in inches (DPI=100)', default=12)
    parser.add_argument('--boundaries', type=ast.literal_eval, help='Boundaries [minlon,maxlon,minlat,maxlat]', default=None)
    parser.add_argument('input', help='The input XML file, or directory containing a {} file'.format(MATERIALS_FILE))

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if not os.path.exists(args.input):
        logging.error('Input path "%s" does not exist', args.input)
        sys.exit(1)

    if os.path.isdir(args.input):
        if args.single:
            directory_to_single_png(args.input,
                outdir=args.output, figsize=[args.width, args.height], boundaries=args.boundaries,
                material=args.material, legend=args.legend,
                edgecolor=args.edgecolor,alpha=args.alpha,
                worldcolor=args.worldcolor, worldshape=args.worldshape)
        else:
            directory_to_png(args.input,
                outdir=args.output, figsize=[args.width, args.height], boundaries=args.boundaries,
                facecolor=args.facecolor, edgecolor=args.edgecolor, alpha=args.alpha,
                worldcolor=args.worldcolor, worldshape=args.worldshape)
    else:
        region_to_png(args.input,
            outdir=args.output, figsize=[args.width, args.height], boundaries=args.boundaries,
            facecolor=args.facecolor, edgecolor=args.edgecolor, alpha=args.alpha,
            worldcolor=args.worldcolor, worldshape=args.worldshape)
