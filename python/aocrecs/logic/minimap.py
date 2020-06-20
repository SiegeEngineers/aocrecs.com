"""Generate SVG minimap."""
from aioify import wrap as aiowrap
from subprocess import Popen, PIPE
import math
import xml.etree.ElementTree as ET

from aocrecs.consts import PREDATOR_IDS, HERDABLE_IDS, HUNT_IDS, BOAR_IDS, FISH_IDS, FORAGE_ID, TC_IDS


GOLD_COLOR = '#FFC700'
STONE_COLOR = '#919191'
FOOD_COLOR = '#A5C46C'
RELIC_COLOR = '#FFFFFF'
CONSTANT_COLORS = [GOLD_COLOR, STONE_COLOR, FOOD_COLOR, RELIC_COLOR]
FOOD_IDS = PREDATOR_IDS + HERDABLE_IDS + HUNT_IDS + BOAR_IDS + FISH_IDS + [FORAGE_ID]
GOLD_ID = 66
STONE_ID = 102
RELIC_ID = 285
OBJECT_MAPPING = [
    ([GOLD_ID], GOLD_COLOR),
    ([STONE_ID], STONE_COLOR),
    (FOOD_IDS, FOOD_COLOR),
    ([RELIC_ID], RELIC_COLOR)
]
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
        'transform': 'translate({}, {}) scale({}, {}) rotate(-45)'.format(0, translate/2, scale, scale/2)
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


@aiowrap
def generate_svg(tiles, dimension, terrain, objects, player_colors, corners=0, squareness=3, scale=1000): # pylint: disable=too-many-arguments
    """Generate map SVG."""
    layers = {}
    from collections import defaultdict
    x = defaultdict(int)
    y = {}
    for i, tile in enumerate(tiles):
        color = terrain[tile['terrain_id']][get_slope(tiles, dimension, i)]
        x[tile['terrain_id']] += 1
        y[tile['terrain_id']] = color
        if color not in layers:
            layers[color] = new_canvas(dimension)
        layers[color][tile['y']][tile['x']] = '1'
    #for t, c in x.items():
    #    print(t, c, y[t])
    for color in list(player_colors.values()) + CONSTANT_COLORS:
        layers[color] = new_canvas(dimension)
    for obj in objects:
        if obj['player_number'] is not None and obj['class_id'] in [70, 80]:
            color = player_colors[obj['player_number']]
            layers[color][int(obj['y'])][int(obj['x'])] = '1'
            if obj['object_id'] in TC_IDS:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        layers[color][int(obj['y']) + i][int(obj['x']) + j] = '1'
            elif obj['object_id'] in [88, 793]:
                for i in range(-1, 2):
                    layers[color][int(obj['y']) + i][int(obj['x'])] = '1'
            elif obj['object_id'] in [64, 789]:
                for i in range(-1, 2):
                    layers[color][int(obj['y'])][int(obj['x']) + i] = '1'
        else:
            for object_ids, color in OBJECT_MAPPING:
                if obj['object_id'] in object_ids:
                    layers[color][int(obj['y'])][int(obj['x'])] = '1'
                    break

    return trace(layers, dimension, corners, squareness, scale)
