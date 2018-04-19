import tcod

from src.config import arrows, vim, movements
from src.maps import same_location, Location, is_walkable
from src.maps.datatypes import Tile
from src.objects.combat import (dice_roll, does_attack_hit,
                                thrown_damage_done_by, make_attack)
from src.objects.datatypes import (Scroll, Armour, Weapon,
                                   Projectile, Potion, Monster,
                                   MagicWand, Food, Fruit)
from src.gui import inventory_menu, controls_menu, message, update_screen


def get_id_action(level):
    update_screen(level)
    key = tcod.console_wait_for_keypress(flush=True)
    while key.vk != 66:
        key = tcod.console_wait_for_keypress(flush=False)
    if key.text == "*":
        inventory_menu(level)
        return get_id_action(level)
    if key.text in level.player.inventory:
        return key.text
    else:
        message("Unknown item")


def get_from_inventory(i, inventory):
    if i is None:
        message("Invalid Key")
        return
    itm = inventory[i]
    if itm is None:
        message("No such item")
    return itm


def takeoff_armour(level):
    if level.player.wearing is not None:
        dfnc = level.player.wearing.defence
        message("Rogue removes {} [{}]".format(level.player.wearing.name,
                                               11-dfnc))
        level.player.wearing = None
    else:
        message("Rogue is already not wearing armour")


def wear_armour(level):
    if level.player.wearing is not None:
        message("Rogue is already wearing armour")
    else:
        message("Wear what?")
        i = get_id_action(level)
        itm = get_from_inventory(i, level.player.inventory)
        if itm is None:
            return
        itm = itm.item
        if type(itm) == Armour:
            level.player.wearing = itm
            message("Rogue puts on {} [{}]".format(itm.name, 11-itm.defence))
        else:
            message("Can't wear {} as armour".format(itm.name))


def wield_weapon(level):
    message("Wield what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        return
    itm = itm.item
    if type(itm) in [Weapon, Projectile]:
        level.player.wielding = itm
        message("Rogue wields {}".format(itm.name))
    else:
        message("Can't wield {} as weapon".format(itm.name))


def decr(itm, letter, inventory):
    itm.count -= 1
    if itm.count == 0:
        inventory[letter] = None
    return itm.item


def drop_item(level):
    message("Drop what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        return
    if itm.item in [level.player.wearing, level.player.wielding]:
        message("Rogue is using {}, can't drop it".format(itm.item.name))
    else:
        if type(itm) == MagicWand:
            itm.count = 1  # Let decr drop the whole wand
        itm = decr(itm, i, level.player.inventory)
        itm.picked_up = False
        itm.location = level.player.location
        level.items.append(itm)
        message("Dropped {}".format(itm.name))


def read_scroll(level):
    message("Read what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        return
    if type(itm.item) == Scroll:
        itm = decr(itm, i, level.player.inventory)
        itm.name.name = itm.name.realname
        return itm.function(level)
    else:
        message("Can't read {}".format(itm.item.name))


def quaff_potion(level):
    message("Quaff what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        return
    if type(itm.item) == Potion:
        itm = decr(itm, i, level.player.inventory)
        itm.name.name = itm.name.realname
        return itm.function(level)
    else:
        message("Can't quaff {}".format(itm.item.name))


def is_direction_key(key):
    is_arrow_key = key.vk in list(arrows)
    is_vim_key = key.vk == 66 and key.text in "hjklyubn"
    return is_arrow_key or is_vim_key


def get_dir_action(level):
    message("direction?")
    update_screen(level)
    key = tcod.console_wait_for_keypress(flush=False)
    while not is_direction_key(key):
        key = tcod.console_wait_for_keypress(flush=False)
    if key.vk in arrows:
        return arrows[key.vk]
    elif key.vk == 66 and key.text in "hjklyubn":
        return vim[key.text]


def find_target(direction, dist, level):
    x, y = level.player.location
    dx, dy = movements[direction]
    for _ in range(dist):
        new_location = Location(x + dx, y + dy)
        if not is_walkable(new_location, level):
            return Location(x, y)
        monsters = [m for m in level.monsters
                    if same_location(m.location, new_location)]
        if len(monsters) > 0:
            return monsters[0]
        x += dx
        y += dy
    return new_location


def throw_item(level):
    target = find_target(get_dir_action(level), 10, level)
    message("Throw what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None or not hasattr(itm, 'item'):
        message("No such item")
        return
    if itm.item in [level.player.wearing, level.player.wielding]:
        message("Rogue is using {}, can't throw it".format(itm.name))
        return
    if type(itm.item) == MagicWand:
        itm.count = 1  # So decr function will do rest of disposing of it
    itm = decr(itm, i, level.player.inventory)
    if type(target) == Location:
        itm.location = target
        level.items.append(itm)
        itm.picked_up = False
        message("Rogue threw {}".format(itm.name))
    elif type(target) == Monster:
        if does_attack_hit(level.player, target, level.number):
            make_attack(level.player, target,
                        thrown_damage_done_by(itm, level.player))
            
        else:
            message("Rogue attacks {} and misses".format(target.name))


def zap_wand(level):
    target = find_target(get_dir_action(level), 8, level)
    message("Zap with what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None or not hasattr(itm, 'item'):
        message("No such wand")
    if not type(itm.item) == MagicWand:
        message("Can't zap with {}".format(itm.item.name))
        return
    if type(target) == Monster:
        itm = decr(itm, i, level.player.inventory)
        message("Rogue zaps {}".format(target.name))
        itm.function(level, target)
    else:
        message("Rogue has no target")


def eat(level):
    message("Eat what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        message("No such food")
    if not type(itm.item) in [Food, Fruit]:
        message("Can't eat {}".format(itm.item.name))
    else:
        itm = decr(itm, i, level.player.inventory)
        message("Rogue eats the {}, it tastes {}".format(itm.name,
                                                         itm.taste))
        itm.function(level)


actions = {"TAKE_OFF_ARMOUR": takeoff_armour,
           "WEAR_ARMOUR": wear_armour,
           "WIELD_WEAPON": wield_weapon,
           "DROP_ITEM": drop_item,
           "INVENTORY": inventory_menu,
           "VIEW_CONTROLS": controls_menu,
           "READ_SCROLL": read_scroll,
           "QUAFF_POTION": quaff_potion,
           "THROW_ITEM": throw_item,
           "ZAP_WAND": zap_wand,
           "EAT": eat,
           }
