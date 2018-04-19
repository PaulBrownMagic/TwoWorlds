from random import randint, choice

import tcod

from src.config import movements, HUNGRY, HUNGRY_DIE, HUNGRY_WEAK, HUNGRY_FEINT
# from src.inputs import movements, get_id_action
from src.maps import (Location,
                      is_blocked,
                      is_walkable,
                      same_location,
                      place_in_room,
                      distance_to)
from src.gui import (message,
                     update_screen,
                     inventory_menu,
                     controls_menu,
                     )
from src.objects.datatypes import (Player, Armour, Weapon, Potion,
                                   Projectile, Scroll, InventoryItem,
                                   MagicWand, Food, Fruit)
from src.objects.weapons import mace, make_weapon, shortbow, arrow
from src.objects.armour import ringmail, make_armour, armours
from src.objects.actions import actions
from src.objects.combat import attack
from src.objects.food import foods, make_food
from src.objects.monsters import monsters_for, make_monster
from src.objects.amulet import is_amulet

# flags: A:armour drain, M:mean, F:flying, H:hidden, R:regen hp,
# V:drain hp, X:drain xp, S:stationairy, L:lure player

move_ticker = 1


def run_move_logic(level, user_input):
    game_state = None
    if level.player.state == "DEAD":
        return "PLAYER_DEAD"
    if user_input in movements:
        tick_move(level)
        if getting_hungry(level.player):
            x, y = movements[user_input]
            _move(level.player, x, y, level)
        for monster in level.monsters:
            monster_move(level, monster)
        find_stairs(level)
        autopickup(level)
        game_state = triggertrap(level)
    elif user_input in actions:
        action_state = actions[user_input](level)
        game_state = action_state if game_state is None else game_state
    return "PLAYING" if game_state is None else game_state


def tick_move(level):
    global move_ticker
    move_ticker += 1
    if move_ticker % 20 == 0:
        for mon in filter(lambda m: "R" in m.flags, level.monsters):
            regen_health(mon, level.number)
        regen_health(level.player, level.number)
    if move_ticker % 50 == 0:
        add_monster(level)
    if move_ticker % 20 == 0 and move_ticker % 50 == 0:
        move_ticker = 1


def add_monster(level):
    new_monster = make_monster(choice(monsters_for(level)))
    place_in_room(level, new_monster)
    while distance_to(level.player.location, new_monster.location) < 24:
        place_in_room(level, new_monster)
    level.monsters.append(new_monster)


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


def incr_hp(monster):
    monster.hp += randint(1, 3)
    if monster.hp > monster.max_hp:
        monster.hp = monster.max_hp


def monster_regens(monster):
    return "R" in monster.flags


def do_hp_regen(level, mt):
    list(map(incr_hp, filter(monster_regens(level.monsters))))
    if level.number < 8:
        return mt % 21 - level.number * 2 == 0
    else:
        return mt % 3 == 0


def regen_health(mo, i):
    if i < 8:
        x = 1
    else:
        x = randint(1, i-7)
    mo.hp = mo.hp + x if mo.hp < mo.max_hp - x else mo.max_hp


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


def is_confused(obj):
    confused = False
    if obj.state == "CONFUSED":
        obj.state = "ACTIVE"
        message("{} is no longer confused".format(obj.name.capitalize()))
    elif obj.state.startswith("CONFUSED"):
        obj.state = obj.state[:-1]
        confused = True
    return confused


def _move(obj, x, y, level, stationary=False):
    if type(obj) == Player and player_sleeping(level):
        return
    if is_confused(obj):
        x, y = movements[choice(list(movements))]
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    if walkable and not blocked and not stationary:
        obj.location = new_location
    if walkable and blocked:
        monsters = filter(lambda x: x.location == new_location and x.blocks,
                          level.monsters + [level.player])
        for monster in monsters:
            attack(obj, monster, level)


def find_stairs(level):
    in_fov = tcod.map_is_in_fov(level.map_grid, level.stairs.location.x,
                                level.stairs.location.y)
    if in_fov:
        level.stairs.found = True


def autopickup(level):
    itms = [item for item in level.items
            if same_location(level.player.location, item.location)]
    for itm in itms:
        pickup(level.player, itm)


def triggertrap(level):
    traps = [trap for trap in level.traps
             if same_location(level.player.location, trap.location)]
    for trap in traps:
        trap.found = True
        return trap.function(level)


def pickup(player, item):
    if same_location(player.location, item.location):
        if is_amulet(item):
            player.has_amulet_of_yendor = True
            message("Rogue picked up The Amulet Of Yendor")
            return
        # See if existing location
        existing = [l for l, i in player.inventory.items()
                    if i is not None and i.item.name == item.name]
        for e in existing:
            if not player.inventory[e].full:
                more_items(item, player.inventory[e])
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
            message("Rogue's inventory is full")


def more_items(item, slot):
    if type(item) in [MagicWand, Projectile]:
        incr = randint(2, 10)
    else:
        incr = 1
    if slot.count + incr < slot.max_count:
        slot.count += incr
    else:
        slot.count = slot.max_count


def make_inventory_item(itm):
    if type(itm) in [Potion, Scroll, Food, Fruit]:
        return InventoryItem(itm, max_count=26)
    elif type(itm) == Projectile:
        return InventoryItem(itm, count=randint(1, 15), max_count=50)
    elif type(itm) == MagicWand:
        return InventoryItem(itm, count=itm.count, max_count=26)
    else:
        return InventoryItem(itm)


def is_flying_targeting(monster):
    return "F" in monster.flags and \
            monster.state == "TARGETING" and \
            randint(1, 10) < 4


def monster_move(level, monster):
    update_monster_state(level, monster)
    stationary = "S" in monster.flags
    is_active = monster.state == "ACTIVE"
    is_confused = monster.state.startswith("CONFUSED")
    if is_active or is_confused or is_flying_targeting(monster):
        x, y = movements[choice(list(movements))]
        _move(monster, x, y, level, stationary)
    elif monster.state == "TARGETING":
        astar = tcod.path_new_using_map(level.map_grid, 1.95)
        tcod.path_compute(astar, monster.location.x, monster.location.y,
                          level.player.location.x, level.player.location.y)
        next_tile = tcod.path_get(astar, 0)
        x, y = (next_tile[0] - monster.location.x,
                next_tile[1] - monster.location.y)
        _move(monster, x, y, level, stationary)

    in_fov = tcod.map_is_in_fov(level.map_grid, monster.location.x,
                                monster.location.y)
    close = distance_to(monster.location, level.player.location) > 2
    if "L" in monster.flags and close and in_fov:
        update_screen(level)
        astar = tcod.path_new_using_map(level.map_grid, 1.95)
        tcod.path_compute(astar,
                          level.player.location.x, level.player.location.y,
                          monster.location.x, monster.location.y)
        next_tile = tcod.path_get(astar, 0)
        x, y = (next_tile[0] - level.player.location.x,
                next_tile[1] - level.player.location.y)
        _move(level.player, x, y, level)


def update_monster_state(level, monster):
    in_fov = tcod.map_is_in_fov(level.map_grid,
                                monster.location.x, monster.location.y)
    if monster.hp <= 0:
        monster.state = "DEAD"
    elif in_fov and monster.state == "SNOOZING" and randint(1, 10) < 10:
        monster.state = "ACTIVE"
    elif in_fov and "M" in monster.flags and randint(1, 10) < 10:
        monster.state = "TARGETING"
    elif in_fov and monster.state == "ACTIVE" and randint(1, 10) < 8:
        monster.state = "TARGETING"


def make_player():
    player = Player(weapon=make_weapon(mace),
                    armour=make_armour(ringmail),
                    items=[make_weapon(shortbow),
                           make_weapon(arrow),
                           make_food(foods[0]),
                           ]
                    )
    for itm in player.inventory.values():
        if itm.item.name == "Arrow":
            itm.count = 30
            break
    return player
