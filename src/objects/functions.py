from random import randint, choice

import tcod

from src.maps import Location, is_blocked, is_walkable  # , same_location
from src.gui import message
from src.objects.datatypes import Player

# flags: A: armour drain, M:mean, F:flying, H: hidden, R: regen hp,
# V: drain hp, X: drain xp, S:stationairy, L: lure player

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


def _move(obj, x, y, level, stationary=False):
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    if walkable and not blocked and not stationary:
        obj.location = new_location
    if walkable and blocked:
        monsters = filter(lambda x: x.location == new_location and x.blocks,
                          level.monsters + [level.player])
        for monster in monsters:
            attack(obj, monster)


def is_flying_targeting(monster):
    return "F" in monster.flags and \
            monster.state == "TARGETING" and \
            randint(1, 10) < 4


def monster_move(level, monster):
    update_monster_state(level, monster)
    stationary = "S" in monster.flags
    if monster.state == "ACTIVE" or is_flying_targeting(monster):
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


def attack(x, y):
    if type(x) == type(y):
        return
    msg = "{} attacks {}".format(x.name, y.name)
    if does_attack_hit(y):
        y.hp -= damage_done_by(x)
        if y.hp <= 0:
            y.state = "DEAD"
            msg += " and defeats it."
            update_xp(x, y)
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


def update_xp(x, y):
    if type(x) == Player:
       x.xp += y.xp
       if x.xp >= x.xp_to_level_up:
            x.xp_level += 1
            x.attack = "{}d4".format(x.xp_level)


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
