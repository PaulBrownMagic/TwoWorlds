from functools import partial
from random import choice, randint

from src.levels.datatypes import Level, MagicLevel
from src.maps import place_in_room
from src.objects import (Stairs,
                         make_monster,
                         monsters_for_level,
                         items_for,
                         get_x_scrolls_for,
                         )


def make_level(world, level_number, player):
    stairs = Stairs()

    level = Level(world,
                  level_number,
                  player,
                  stairs,
                  [],
                  [],
                  )
    range_monsters = monsters_for_level(level)
    monsters = [make_monster(choice(range_monsters))
                for _ in range(randint(4, 8))]
    level.monsters = monsters
    level.items = items_for(level) + get_x_scrolls_for(level, randint(1, 4))
    place = partial(place_in_room, level.map_grid)
    place(stairs)
    list(map(place, level.monsters))
    list(map(place, level.items))
    return level


def is_alive(obj):
    return obj.state != "DEAD"


def not_picked_up(item):
    return not item.picked_up


def update_level(level):
    level.monsters = list(filter(is_alive, level.monsters))
    level.items = list(filter(not_picked_up, level.items))
