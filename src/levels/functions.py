from functools import partial
from random import choice, randint

from src.levels.datatypes import Level, MagicLevel
from src.maps import place_in_room
from src.objects import (Stairs,
                         get_x_armours,
                         get_x_weapons,
                         get_x_monsters_for,
                         get_x_scrolls_for,
                         get_x_potions,
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

    level.monsters = get_x_monsters_for(randint(4, 8), level)
    level.items = get_x_armours(randint(0, 3))
    level.items += get_x_weapons(randint(0, 3))
    level.items += get_x_scrolls_for(randint(1, 4), level)
    level.items += get_x_potions(randint(1, 4))

    place = partial(place_in_room, level)
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
