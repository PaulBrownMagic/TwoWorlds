from functools import partial
from random import choice, randint

import tcod

from src.config import (arrows, vim, movements,
                        HUNGRY, HUNGRY_DIE, HUNGRY_WEAK, HUNGRY_FEINT)
from src.maps import same_location, Location, is_walkable, is_blocked

from src.maps.datatypes import Tile
from src.objects.combat import (dice_roll, does_attack_hit,
                                thrown_damage_done_by, make_attack)
from src.objects.datatypes import (Scroll, Armour, Weapon, Player,
                                   Projectile, Potion, Monster,
                                   MagicWand, Food, Fruit, InventoryItem)
from src.gui import inventory_menu, controls_menu, message, update_screen
from src.objects.amulet import is_amulet
from src.objects.combat import attack


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
        if does_attack_hit(level.player, target, level.number, itm):
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
        if target.state in ["SLEEPING", "SNOOZING"]:
            target.state = "ACTIVE"
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


def autopickup(level):
    itms = [item for item in level.items
            if same_location(level.player.location, item.location)]
    for itm in itms:
        pickup(level.player, itm)


def pickup(player, item):
    if same_location(player.location, item.location):
        if is_amulet(item):
            player.has_amulet_of_yendor = True
            message("Rogue picked up The Amulet Of Yendor")
            return
        if is_scare_monster(item):
            if item.used_up:
                message("The scroll crumbles away to nothing")
                return
            else:
                item.used_up = True
        # See if existing location
        existing = [l for l, i in player.inventory.items()
                    if i is not None and i.item.name == item.name]
        for e in existing:
            if not player.inventory[e].full:
                more_items(item, player.inventory, e)
                item.picked_up = True
                message("Rogue picked up {} ({})".format(item.name, e))
                return
        # Or add to new slot
        spaces = [l for l, i in player.inventory.items() if i is None]
        overburdened = sum([i.weight for i in player.inventory.values()
                            if i is not None]) >= player.inventory_limit
        if len(spaces) > 0 and not overburdened:
            player.inventory[spaces[0]] = make_inventory_item(item)
            item.picked_up = True
            item.found = False
            if is_amulet(item):
                player.has_amulet_of_yendor = True
            message("Rogue picked up {} ({})".format(item.name, spaces[0]))
        else:
            message("Inventory is full, moved onto {}".format(item.name))


def more_items(item, inventory, slot):
    if type(item) == MagicWand:
        incr = randint(2, 10)
    else:
        incr = 1
    inventory[slot].count += incr


def make_inventory_item(itm):
    if type(itm) in [Potion, Scroll, Food, Fruit]:
        return InventoryItem(itm, max_count=26)
    elif type(itm) == Projectile:
        return InventoryItem(itm, count=randint(1, 15), max_count=50)
    elif type(itm) == MagicWand:
        return InventoryItem(itm, count=itm.count, max_count=26)
    else:
        return InventoryItem(itm)


def is_scare_monster(item):
    if hasattr(item.name, "realname"):
        return item.name.realname == "a Scroll of Scare Monster"
    else:
        return False


def is_functioning(item):
    return hasattr(item, "function")


def monsters_are_scared(level):
    on_tile = partial(same_location, level.player.location)
    itms = list(filter(is_scare_monster,
                       filter(is_functioning,
                              [item for item in level.items
                               if on_tile(item.location)])))
    return True if len(itms) > 0 else False


def getting_hungry(player):
    player.hunger += 1
    if player.hunger == HUNGRY:
        message("Rogue is hungry")
    if player.hunger == HUNGRY_WEAK:
        message("Rogue is weak")
    if player.hunger in HUNGRY_FEINT:
        message("Rogue is faint")
        return False  # Can't move
    if player.hunger > HUNGRY_DIE:
        player.state = "DEAD"
    return True  # Move


def move_no_pickup(level):
    if getting_hungry(level.player):
        x, y = movements[get_dir_action(level)]
        _move(level.player, x, y, level)


def _move(obj, x, y, level, stationary=False):
    if type(obj) == Player and player_sleeping(level):
        return False
    if is_confused(obj):
        x, y = movements[choice(list(movements))]
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    scared = monsters_are_scared(level)
    if walkable and not blocked and not stationary:
        obj.location = new_location
        return True
    elif walkable and blocked and not (type(obj) == Monster and
                                       scared):
        monsters = filter(lambda x: x.location == new_location and x.blocks,
                          level.monsters + [level.player])
        for monster in monsters:
            attack(obj, monster, level)
        return False


def is_confused(obj):
    confused = False
    if obj.state == "CONFUSED":
        obj.state = "ACTIVE"
        message("{} is no longer confused".format(obj.name.capitalize()))
    elif obj.state.startswith("CONFUSED"):
        obj.state = obj.state[:-1]
        confused = True
    return confused


def player_sleeping(level):
    player = level.player
    sleeping = False
    if player.state == "SLEEP":
        player.state = "ACTIVE"
        message("Rogue awakens")
    elif player.state.startswith("SLEEP"):
        message("Rogue sleeps")
        player.state = player.state[:-1]
        sleeping = True
    return sleeping


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
           "PICK_UP_ITEM": autopickup,
           "MOVE_WITHOUT_PICKING_UP": move_no_pickup,
           }
