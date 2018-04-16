from functools import partial
from random import choice, randint

from src.levels.datatypes import Level, MagicLevel
from src.maps import place_in_room
from src.objects import Stairs, make_monster, monsters_for_level


def make_level(level_number, player):
    stairs = Stairs()

    level = Level(level_number,
                  player,
                  stairs,
                  [],
                  [],
                  )
    range_monsters = monsters_for_level(level)
    monsters = [make_monster(choice(range_monsters))
                for _ in range(randint(4, 8))]
    level.monsters = monsters
    place = partial(place_in_room, level.map_grid)
    place(stairs)
    list(map(place, level.monsters))
    return level


def is_alive(obj):
    return obj.state != "DEAD"


def update_level(level):
    level.monsters = list(filter(is_alive, level.monsters))
