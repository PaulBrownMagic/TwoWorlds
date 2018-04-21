from itertools import chain, product
from math import sqrt
from random import choice


def place_in_room(level, obj):
    mp = level.map_grid
    occupied_locations = [itm.location
                          for itm in level.items + level.monsters
                          if hasattr(itm, "location")]
    tile = choice([tile for rm in mp.rooms
                   for tile in chain(*rm.tiles)
                   if tile.location not in occupied_locations
                   and tile.walkable])
    obj.location = tile.location


def same_location(l1, l2):
    return l1 == l2


def in_same_room(l1, l2, mp):
    for room in mp.rooms:
        tiles = chain(*room.tiles)
        locations = [tile.location for tile in tiles]
        if l1 in locations and l2 in locations:
            return True
    return False


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


def adjacent_tiles(location, level):
    mp = level.map_grid
    x, y = location
    adj = [(x, y) for x, y in product([-1, 0, 1], [-1, 0, 1])
           if (x, y) != (0, 0)]
    return [mp.tiles[y+dy][x+dx] for dx, dy in adj]
