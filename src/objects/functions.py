from functools import partial
from random import randint, choice

import tcod

from src.config import movements
# from src.inputs import movements, get_id_action
from src.maps import (Location,
                      is_blocked,
                      is_walkable,
                      same_location,
                      place_in_room,
                      distance_to,
                      in_same_room)
from src.gui import (message,
                     update_screen,
                     inventory_menu,
                     controls_menu,
                     )
from src.objects.datatypes import (Player, Armour, Weapon, Potion,
                                   Projectile, Scroll, InventoryItem,
                                   MagicWand, Food, Fruit, Monster)
from src.objects.weapons import mace, make_weapon, shortbow, arrow
from src.objects.armour import ringmail, make_armour, armours
from src.objects.actions import (actions,
                                 autopickup,
                                 _move,
                                 getting_hungry,
                                 )
from src.objects.food import foods, make_food
from src.objects.monsters import monsters_for, make_monster
from src.objects.armour import get_x_armours
from src.objects.magicwands import get_x_wands
from src.objects.potions import get_x_potions
from src.objects.scrolls import get_x_scrolls_for
from src.objects.weapons import get_x_weapons

# flags: A:armour drain, M:mean, F:flying, H:hidden, R:regen hp,
# V:drain hp, X:drain xp, S:stationairy, L:lure player

move_ticker = 1


def run_move_logic(level, user_input):
    game_state = None
    if level.player.state == "DEAD":
        return "PLAYER_DEAD"
    if user_input in movements:
        if getting_hungry(level.player):
            x, y = movements[user_input]
            if _move(level.player, x, y, level) and (x, y) != (0, 0):
                autopickup(level)
    elif user_input in actions:
        game_state = actions[user_input](level)
    else:  # Input not recognised, no real turn
        return "PLAYING"
    # Carry on with the turn
    find_stairs(level)
    game_state = triggertrap(level) if game_state is None else game_state
    tick_move(level)
    for monster in level.monsters:
        if monster.state == "DEAD":
            monster_drop(monster, level)
        else:
            monster_move(level, monster)
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
    new_monster.state = "ACTIVE"
    place_in_room(level, new_monster)
    while distance_to(level.player.location, new_monster.location) < 24:
        place_in_room(level, new_monster)
    level.monsters.append(new_monster)


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


def find_stairs(level):
    in_fov = tcod.map_is_in_fov(level.map_grid, level.stairs.location.x,
                                level.stairs.location.y)
    if in_fov:
        level.stairs.found = True


def triggertrap(level):
    traps = [trap for trap in level.traps
             if same_location(level.player.location, trap.location)]
    for trap in traps:
        trap.found = True
        return trap.function(level)


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
    in_player_room = in_same_room(level.player.location,
                                  monster.location,
                                  level.map_grid)
    if monster.hp <= 0:
        monster.state = "DEAD"
    elif in_fov and monster.state == "SNOOZING" and randint(1, 10) < 10:
        monster.state = "ACTIVE"
    elif (in_fov or in_player_room) and "M" in monster.flags and randint(1, 10) < 10:
        monster.state = "TARGETING"
    elif in_fov and monster.state == "ACTIVE" and randint(1, 10) < 8:
        monster.state = "TARGETING"



def monster_drop(monster, level):
    if type(monster) == Monster and randint(1, 100) <= monster.carry:
        item = monster_drop_item(level)
        item.location = monster.location
        level.items.append(item)


def monster_drop_item(level):
    if level.world == "NORMAL":
        wrl = get_x_weapons(1) + get_x_armours(1)
    else:
        wrl = get_x_wands(1)
    return choice(wrl + get_x_potions(1) + get_x_scrolls_for(1, level))


def make_player():
    sb = make_weapon(shortbow)
    sb.attack_mod = 1
    sb.dexterity_mod = 1
    sb.realname = "[+1] [+1] {}".format(sb.name)
    sb.name = sb.realname
    ar = make_weapon(arrow)
    ar.attack_mod = 0
    ar.dexterity_mod = 0
    ar.realname = "[+0] [+0] {}".format(ar.name)
    ar.name = ar.realname
    mc = make_weapon(mace)
    mc.attack_mod = 2
    mc.dexterity_mod = 2
    mc.realname = "[+2] [+2] {}".format(mc.name)
    mc.name = mc.realname
    player = Player(weapon=mc,
                    armour=make_armour(ringmail),
                    items=[sb,
                           ar,
                           make_food(foods[0]),
                           ]
                    )
    player.inventory['d'].count = 30
    return player
