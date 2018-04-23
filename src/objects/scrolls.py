from itertools import chain
from math import ceil
from random import choice, randint, choices

from tcod import color as colour

from src.config import movements
from src.gui import message
from src.maps import distance_to, place_in_room
from src.inputs import get_id_action
# from src.characters.actions import get_from_inventory, decr
from src.objects.datatypes import Scroll, ScrollName
from src.characters.functions import _move
# from src.objects.monsters import monsters_for, make_monster

S_COLOUR = colour.white


def confuse_next_monster(level):
    message("Rogue's hands glow red for a moment")
    level.player.state = "CONFUSE_NEXT_MONSTER"


def view_whole_map(level):
    message("This scroll seems to have a map on it")
    for tile in chain(*level.map_grid.tiles):
        tile.explored = True


def hold_monster(level):
    """Freezes nearby monsters"""
    message("Nearby monsters freeze")
    close_by = [m for m in level.monsters
                if distance_to(level.player.location, m.location) < 6]
    for m in close_by:
        m.flags.append("S")


def sleep(level):
    """Reader sleeps"""
    message("Rogue feels drowzy")
    level.player.state = "SLEEP123"


def enchant_armour(level):
    if level.player.wearing is not None:
        message("Rogue's armour glows blue for a moment")
        level.player.wearing.defence -= 1
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
    itm = itm.item
    if hasattr(itm.name, "realname"):
        itm.name.name = itm.name.realname
    elif hasattr(itm, "realname"):
        itm.name = itm.realname
    message("You identified {}".format(itm.name))


def read_scare_monster(level):
    message("You hear manical laughter in the distance")


def teleport(level):
    """Teleport player"""
    place_in_room(level, level.player)
    message("You have been transported")


def enchant_weapon(level):
    name = level.player.wielding.name
    message("Rogue's {} glows blue for a second".format(name))
    """
    atck = level.player.wielding.attack
    dice, sides = map(int, atck.split('d'))
    total = dice * sides
    dice += 1
    sides = ceil(total/dice)
    level.player.wielding.attach = "{}d{}".format(dice, sides)
    """
    if randint(0, 1) == 0:
        level.player.wielding.attack_mod += 1
    else:
        level.player.wielding.dexterity_mod += 1


def create_monster(level):
    monster = make_monster(choice(monsters_for(level)))
    monster.state = "TARGETING"
    monster.location = level.player.location
    for _ in range(5):
        if monster.location == level.player.location:
            x, y = movements[choice(list(movements))]
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


def transition_worlds(level):
    message("Everything turns dark, you awaken in a new world")
    return "TOGGLE_WORLDS"


N = "NORMAL"
M = "MAGIC"

Name = ScrollName
scrolls = [dict(name=Name('Mapping'), world=N, p=4, f=view_whole_map),
           dict(name=Name('Confuse Monster'), world=N, p=7,
                f=confuse_next_monster),
           dict(name=Name('Hold Monster'), world=M, p=2, f=hold_monster),
           dict(name=Name('Sleep'), world=M, p=3, f=sleep),
           dict(name=Name("Enchant Armour"), world=M, p=7, f=enchant_armour),
           dict(name=Name("Identity"), world=N, p=7, f=identify),
           dict(name=Name("Scare Monster"), world=M, p=3,
                f=read_scare_monster),
           dict(name=Name("Teleportation"), world=M, p=5, f=teleport),
           dict(name=Name("Enchant Weapon"), world=M, p=8, f=enchant_weapon),
           # dict(name=Name("Create Monster"), world=M, p=4, f=create_monster),
           # dict(name=Name("Remove Curse"), world=M, p=7, f=remove_curse),
           dict(name=Name("Aggravate Monsters"), world=N, p=3,
                f=aggravate_monsters),
           dict(name=Name("Protect Armour"), world=M, p=2, f=protect_armour),
           dict(name=Name("Through The Veil"), world=N, p=4,
                f=transition_worlds),
           ]


def make_scroll(s):
    return Scroll(name=s['name'],
                  char="?",
                  colour=S_COLOUR,
                  function=s['f']
                  )


def get_x_scrolls_for(num, level):
    allowed_scrolls = [s for s in scrolls if s['world'] == level.world]
    weights = [s['p'] for s in allowed_scrolls]
    return list(map(make_scroll, choices(allowed_scrolls, weights, k=num)))
