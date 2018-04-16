from itertools import chain
from math import sqrt
from random import choice


def place_in_room(mp, obj):
    tile = choice([tile for rm in mp.rooms for tile in chain(*rm.tiles)])
    obj.location = tile.location


def same_location(l1, l2):
    return l1 == l2


def is_walkable(location, level):
    if level.map_grid.walkable[location.y][location.x]:
        return True
    else:
        return False


def is_blocked(location, level):
    if same_location(location, level.player.location):
        return True

    def on_tile(o):
        return same_location(location, o.location)
    return any([ob.blocks for ob in filter(on_tile, level.all_objects)])


def distance_to(loc1, loc2):
    return sqrt((loc1.x - loc2.x)**2 + (loc1.y - loc2.y)**2)
