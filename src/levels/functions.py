from functools import partial
from random import choice, randint, choices

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

    if world == "NORMAL":
        amount_food = randint(0, 1) if player.hunger > 100 else randint(1, 2)
        level.items = get_x_foods(amount_food)
        add_normal_items(level)
    else:
        level.items = []
        add_magic_items(level)
    if level.number > 25 and not level.player.has_amulet_of_yendor:
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
    armours = get_x_armours(5)
    weapons = get_x_weapons(5)
    scrolls = get_x_scrolls_for(5, level)
    potions = get_x_potions(5)
    weights = [1, 1, 4, 5]
    banks = choices([armours, weapons, scrolls, potions],
                    weights,
                    k=randint(1, 5))
    add_from_banks(level, banks)


def add_magic_items(level):
    scrolls = get_x_scrolls_for(6, level)
    potions = get_x_potions(6)
    wands = get_x_wands(6)
    weights = [2, 2, 1]
    banks = choices([scrolls, potions, wands], weights, k=randint(2, 6))
    add_from_banks(level, banks)


def add_from_banks(level, banks):
    for bank in banks:
        itm = choice(bank)
        level.items.append(itm)


def is_alive(obj):
    return obj.state != "DEAD"


def not_picked_up(item):
    return not item.picked_up


def update_level(level):
    level.monsters = list(filter(is_alive, level.monsters))
    level.items = list(filter(not_picked_up, level.items))
