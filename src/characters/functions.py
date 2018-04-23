from random import randint, choice

import tcod

from src.config import movements
from src.maps import (is_transparent,
                      same_location,
                      place_in_room,
                      distance_to,
                      in_same_room,
                      in_fov)
from src.gui import update_screen

from src.characters.datatypes import Player, Monster
from src.characters.actions import (actions,
                                    autopickup,
                                    _move,
                                    getting_hungry,
                                    )
from src.characters.monsters import monsters_for, make_monster


def player_move(level, direction):
    if getting_hungry(level.player):
        x, y = direction
        if _move(level.player, x, y, level) and (x, y) != (0, 0):
            autopickup(level)


def player_surroundings(level):
    return triggertrap(level)


def add_monster(level):
    new_monster = make_monster(choice(monsters_for(level)))
    new_monster.state = choice(["ACTIVE", "TARGETING"])
    place_in_room(level, new_monster)
    for _ in range(10):
        if distance_to(level.player.location, new_monster.location) < 24:
            place_in_room(level, new_monster)
        else:
            break
    if distance_to(level.player.location, new_monster.location) < 24:
        level.monsters.append(new_monster)


def incr_hp(monster):
    monster.hp += randint(1, 3)
    if monster.hp > monster.max_hp:
        monster.hp = monster.max_hp


def monster_regens(monster):
    return "R" in monster.flags


def regen_health(mo, i):
    if i < 8:
        x = 1
    else:
        x = randint(1, i-7)
    mo.hp = mo.hp + x if mo.hp < mo.max_hp - x else mo.max_hp


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
        diag = 1.95 if is_transparent(monster.location, level) else 0
        try:
            astar = tcod.path_new_using_map(level.map_grid, diag)
            tcod.path_compute(astar, monster.location.x, monster.location.y,
                              level.player.location.x, level.player.location.y)
            next_tile = tcod.path_get(astar, 0)
        except:
            print("ASTAR FAILURE")
            next_tile = (randint(-1, 1), randint(-1, 1))
        x, y = (next_tile[0] - monster.location.x,
                next_tile[1] - monster.location.y)
        _move(monster, x, y, level, stationary)

    close = distance_to(monster.location, level.player.location) > 2
    if "L" in monster.flags and close and in_fov(monster.location, level):
        update_screen(level)
        try:
            astar = tcod.path_new_using_map(level.map_grid, 1.95)
            tcod.path_compute(astar,
                              level.player.location.x, level.player.location.y,
                              monster.location.x, monster.location.y)
            next_tile = tcod.path_get(astar, 0)
        except:
            print("ASTAR FAILURE")
            next_tile = (randint(-1, 1), randint(-1, 1))
        x, y = (next_tile[0] - level.player.location.x,
                next_tile[1] - level.player.location.y)
        _move(level.player, x, y, level)


def update_monster_state(level, monster):
    fov = in_fov(monster.location, level)
    in_player_room = in_same_room(level.player.location,
                                  monster.location,
                                  level.map_grid)
    if monster.hp <= 0:
        monster.state = "DEAD"
    elif fov and monster.state == "SNOOZING" and randint(1, 10) < 9:
        monster.state = "ACTIVE"
    elif (fov or in_player_room) and "M" in monster.flags and randint(1, 10) < 10:
        monster.state = "TARGETING"
    elif fov and monster.state == "ACTIVE" and randint(1, 10) < 8:
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
