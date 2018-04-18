import tcod

from src.objects.datatypes import Scroll, Armour, Weapon, Projectile, Potion
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
        elif type(itm) == Armour:
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
    elif type(itm) in [Weapon, Projectile]:
        level.player.wielding = itm
        message("Rogue wields {}".format(itm.name))
    else:
        message("Can't wield {} as weapon".format(itm.name))


def drop_item(level):
    message("Drop what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        return
    if itm in [level.player.wearing, level.player.wielding]:
        message("Rogue is using {}, can't drop it".format(itm.name))
    else:
        level.player.inventory[i] = None
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
    if type(itm) == Scroll:
        level.player.inventory[i] = None
        itm.name.name = itm.name.realname
        return itm.function(level)
    else:
        message("Can't read {}".format(itm.name))


def quaff_potion(level):
    message("Quaff what?")
    i = get_id_action(level)
    itm = get_from_inventory(i, level.player.inventory)
    if itm is None:
        return
    if type(itm) == Potion:
        level.player.inventory[i] = None
        itm.name.name = itm.name.realname
        return itm.function(level)
    else:
        message("Can't quaff {}".format(itm.name))


actions = {"TAKE_OFF_ARMOUR": takeoff_armour,
           "WEAR_ARMOUR": wear_armour,
           "WIELD_WEAPON": wield_weapon,
           "DROP_ITEM": drop_item,
           "INVENTORY": inventory_menu,
           "VIEW_CONTROLS": controls_menu,
           "READ_SCROLL": read_scroll,
           "QUAFF_POTION": quaff_potion,
           }
