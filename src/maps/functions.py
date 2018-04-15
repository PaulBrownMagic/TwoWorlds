from itertools import chain
from random import choice

from src.maps.datatypes import Map
from src.objects.datatypes import Object


def place_in_room(mp: Map, obj: Object):
    tile = choice([tile for rm in mp.rooms for tile in chain(*rm.tiles)])
    obj.location = tile.location
