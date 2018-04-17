from itertools import chain
from math import ceil
from random import choice, randint

from tcod import color as colour

from src.gui import message
from src.maps import distance_to, place_in_room
from src.objects.datatypes import Scroll
from src.objects.functions import (get_id_action,
                                   get_from_inventory,
                                   movements,
                                   _move)
from src.objects.monsters import monsters_for_level, make_monster

S_COLOUR = colour.white


def confuse_next_monster(level):
    pass


def view_whole_map(level):
    message("This scroll seems to have a map on it")
    for tile in chain(*level.map_grid.tiles):
        tile.explored = True


def hold_monster(level):
    """Freezes nearby monsters"""
    message("Nearby monsters freeze")
    ploc = level.player.location
    close_by = [m for m in level.monsters
                if distance_to(ploc, m.loc) < 6]
    for m in close_by:
        m.flags.append("S")


def sleep(level):
    """Reader sleeps"""
    pass


def enchant_armour(level):
    if level.player.wearing is not None:
        message("Rogue's armour glows blue for a moment")
        level.player.wearing.armour -= 1
    else:
        message("Nothing happens")


def identify(level):
    message("What would you like to identify?")
    key = get_id_action(level)
    while key is None:
        key = get_id_action(level)
    itm = get_from_inventory(key, level.player.inventory)
    if itm is None:
        message("No such item, try again.")
        return identify(level)
    else:
        itm.name = itm.realname
        message("You identified {}".format(itm.name))


def read_scare_monster(level):
    message("You hear manical laughter in the distance")


def teleport(level):
    """Teleport player"""
    place_in_room(level.map_grid, level.player)


def enchant_weapon(level):
    name = level.player.wielding.name
    message("Rogue's {} glows blue for a second".format(name))
    atck = level.player.wielding.attack
    dice, sides = map(int, atck.split('d'))
    total = dice * sides
    dice += 1
    sides = ceil(total/dice)
    level.player.wielding.attach = "{}d{}".format(dice, sides)


def create_monster(level):
    monster = make_monster(choice(monsters_for_level(level)))
    monster.state = "TARGETING"
    monster.location = level.player.location
    for _ in range(5):
        if monster.location == level.player.location:
            x, y = choice(movements.values())
            _move(monster, x, y, level)
        else:
            level.monsters.append(monster)
            message("A {} appeared".format(monster.name))
            return
    message("You hear a feint cry in the distance")


def remove_curse(level):
    pass


def aggravate_monsters(level):
    message("You hear a high pitch humming noise")
    for monster in level.monsters:
        monster.state = "TARGETING"


def protect_armour(level):
    message("Rogue's armour glows gold for a second")
    level.player.wearing.protected = True


N = "NORMAL"
M = "MAGIC"

scrolls = [dict(name='Mapping', world=N, p=4, f=view_whole_map),
           # dict(name='Confuse Monster', world=N, p=7, f=confuse_next_monster),
           dict(name='Hold Monster', world=M, p=2, f=hold_monster),
           # dict(name='Sleep', world=M, p=3, f=sleep),
           dict(name="Enchant Armour", world=M, p=7, f=enchant_armour),
           dict(name="Identity", world=N, p=20, f=identify),
           dict(name="Scare Monster", world=M, p=3, f=read_scare_monster),
           dict(name="Teleportation", world=M, p=5, f=teleport),
           dict(name="Enchant Weapon", world=M, p=8, f=enchant_weapon),
           dict(name="Create Monster", world=M, p=4, f=create_monster),
           # dict(name="Remove Curse", world=M, p=7, f=remove_curse),
           dict(name="Aggravate Monsters", world=N, p=3, f=aggravate_monsters),
           dict(name="Protect Armour", world=M, p=2, f=protect_armour)
           ]


def make_scroll(s):
    return Scroll(name="A scroll titled {}".format(s['name']),
                  realname="Scroll of {}".format(s['name']),
                  char="?",
                  colour=S_COLOUR,
                  function=s['f']
                  )


def get_x_scrolls_for(level, num):
    allowed_scrolls = [s for s in scrolls if s['world'] == level.world]
    max_roll = sum([s['p'] for s in allowed_scrolls])
    scrolls_for_level = []
    for _ in range(num):
        roll = randint(0, max_roll)
        cumulative = 0
        for s in allowed_scrolls:
            cumulative
            if cumulative <= roll <= cumulative + s['p']:
                scrolls_for_level.append(s)
                continue
            cumulative += s['p']
    return list(map(make_scroll, scrolls_for_level))
