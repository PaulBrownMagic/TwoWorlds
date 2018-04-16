from random import randint, choice

import tcod

from src.maps import Location, is_blocked, is_walkable, same_location
from src.gui import message

movements = {"UP": (0, -1),
             "DOWN": (0, 1),
             "LEFT": (-1, 0),
             "RIGHT": (1, 0),
             "UR": (1, -1),
             "UL": (-1, -1),
             "DL": (-1, 1),
             "DR": (1, 1),
             "WAIT": (0, 0),
             }


def run_move_logic(level, user_input):
    if user_input in movements:
        x, y = movements[user_input]
        _move(level.player, x, y, level)
        for monster in level.monsters:
            monster_move(level, monster)



def _move(obj, x, y, level):
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    if walkable and not blocked:
        obj.location = new_location
    if walkable and blocked:
        monsters = filter(lambda x: x.location == new_location and x.blocks,
                          level.monsters + [level.player])
        for monster in monsters:
            attack(obj, monster)


def monster_move(level, monster):
    in_fov = tcod.map_is_in_fov(level.map_grid,
                          monster.location.x, monster.location.y)
    if in_fov and monster.state == "SNOOZING" and randint(1, 10) < 10:
        monster.state = "ACTIVE"
    elif in_fov and monster.state == "ACTIVE":
        monster.state = "TARGETING"
    if monster.state == "ACTIVE":
        x, y = movements[choice(list(movements))]
        _move(monster, x, y, level)
    elif monster.state == "TARGETING":
        astar = tcod.path_new_using_map(level.map_grid, 1.95)
        tcod.path_compute(astar, monster.location.x, monster.location.y,
                          level.player.location.x, level.player.location.y)
        next_tile = tcod.path_get(astar, 0)
        x, y = (next_tile[0] - monster.location.x,
                next_tile[1] - monster.location.y)
        _move(monster, x, y, level)


def attack(x, y):
    if type(x) == type(y):
        return
    msg = "{} attacks {}".format(x.name, y.name)
    if does_attack_hit(y):
        y.hp -= damage_done_by(x)
        if y.hp <= 0:
            y.state = "DEAD"
            msg += " and defeats it."
        else:
            msg += " and hits."
    else:
        msg += " and misses."
    message(msg)


def does_attack_hit(x):
    return randint(1, 20) > x.armour


def damage_done_by(x):
    return dice_roll(x.attack) + x.strength


def dice_roll(dice):
    count, sides = map(int, dice.split('d'))
    return sum([randint(1, sides) for _ in range(count)])
