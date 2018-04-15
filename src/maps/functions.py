from itertools import chain
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
    def on_tile(o):
        return same_location(location, o.location)
    return any([ob.blocks for ob in filter(on_tile, level.all_objects)])
