"""Generate SVG minimap."""

from subprocess import Popen, PIPE
import math
import xml.etree.ElementTree as ET


NAMESPACE = 'http://www.w3.org/2000/svg'


def make_pbm(data, dimension, multiplier):
    """Produce PBM file contents."""
    pbm = 'P1\n{} {}\n'.format(dimension * multiplier, dimension * multiplier)
    for row in data:
        for _ in range(0, multiplier):
            for col in row:
                pbm += (col * multiplier)
    return str.encode(pbm)


def new_canvas(dimension, value='0'):
    """Produce a blank canvas."""
    return [[value] * dimension for _ in range(0, dimension)]


def get_slope(tiles, dimension, i):
    """Compute tile slope.

    TODO: (literal) edge cases
    """
    slope = 'level'
    elevation = tiles[i]['elevation']
    se_tile = i + dimension + 1
    sw_tile = i + dimension - 1
    ne_tile = i - dimension + 1
    nw_tile = i - dimension - 1
    if se_tile < (dimension * dimension) and sw_tile < (dimension * dimension):
        se_elevation = tiles[se_tile]['elevation']
        sw_elevation = tiles[sw_tile]['elevation']
        ne_elevation = tiles[ne_tile]['elevation']
        nw_elevation = tiles[nw_tile]['elevation']
        if nw_elevation > elevation or ne_elevation > elevation:
            slope = 'up'
        if se_elevation > elevation or sw_elevation > elevation:
            slope = 'down'
    return slope


def trace(layers, dimension, corners, squareness, scale):
    """Trace map layers."""
    scale /= squareness
    scale /= dimension
    translate = math.sqrt(((dimension * squareness * scale)**2) * 2)/2.0
    ET.register_namespace('', NAMESPACE)
    svg = ET.Element('svg', attrib={
        'viewBox': '0 0 {} {}'.format(translate * 2, translate),
    })
    transform = ET.SubElement(svg, 'g', attrib={
        'transform': 'translate({}) scale({}, {}) rotate(45)'.format(translate, scale, scale/2)
    })

    for color, canvas in layers.items():
        canvas = layers[color]
        args = ['potrace', '-s', '-a', str(corners)]
        xml = ET.fromstring(Popen(
            args, stdout=PIPE, stdin=PIPE, stderr=PIPE
        ).communicate(input=make_pbm(canvas, dimension, squareness))[0].decode('ascii'))
        layer = xml.find('{' + NAMESPACE + '}g')
        layer.set('fill', color)
        for path in layer.findall('{' + NAMESPACE + '}path'):
            path.set('stroke', color)
            path.set('stroke-width', str(10))
        transform.append(layer)
    return ET.tostring(svg, encoding='unicode')


def generate_svg(tiles, dimension, terrain, corners=0, squareness=3, scale=1000): # pylint: disable=too-many-arguments
    """Generate map SVG."""
    layers = {}
    for i, tile in enumerate(tiles):
        color = terrain[tile['terrain_id']][get_slope(tiles, dimension, i)]
        if color not in layers:
            layers[color] = new_canvas(dimension)
        layers[color][tile['y']][tile['x']] = '1'
    return trace(layers, dimension, corners, squareness, scale)
