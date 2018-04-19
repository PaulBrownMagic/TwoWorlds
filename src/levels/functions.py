from functools import partial
from random import choice, randint

from src.levels.datatypes import Level
from src.maps import place_in_room
from src.objects import (Stairs,
                         get_x_armours,
                         get_x_weapons,
                         get_x_monsters_for,
                         get_x_scrolls_for,
                         get_x_potions,
                         get_x_traps_for,
                         get_x_wands,
                         get_x_foods,
                         get_amulet
                         )


def make_level(world, level_number, player):
    stairs = Stairs()
    level = Level(world,
                  level_number,
                  player,
                  stairs,
                  )

    amount_of_food = randint(0, 2) if player.hunger > 200 else randint(1, 3)
    level.items = get_x_foods(amount_of_food)
    if world == "NORMAL":
        add_normal_items(level)
    else:
        add_magic_items(level)
    if level.number > 25:
        level.items.append(get_amulet())

    level.monsters = get_x_monsters_for(randint(4, 8), level)
    level.traps = get_x_traps_for(randint(0, 2+level.number//4), level)

    place = partial(place_in_room, level)
    place(stairs)
    list(map(place, level.monsters))
    list(map(place, level.items))
    list(map(place, level.traps))
    return level


def add_normal_items(level):
    level.items += get_x_armours(randint(0, 3))
    level.items += get_x_weapons(randint(0, 3))
    level.items += get_x_scrolls_for(randint(1, 4), level)
    level.items += get_x_potions(randint(0, 3))


def add_magic_items(level):
    level.items += get_x_scrolls_for(randint(1, 4), level)
    level.items += get_x_potions(randint(1, 4))
    level.items += get_x_wands(randint(0, 3+level.number//4))


def is_alive(obj):
    return obj.state != "DEAD"


def not_picked_up(item):
    return not item.picked_up


def update_level(level):
    level.monsters = list(filter(is_alive, level.monsters))
    level.items = list(filter(not_picked_up, level.items))
