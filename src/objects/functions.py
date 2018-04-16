from random import randint

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


def _move(obj, x, y, level):
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    if walkable and not blocked:
        obj.location = new_location
    if walkable and blocked:
        monsters = filter(lambda x: x.location == new_location and x.blocks,
                          level.monsters)
        for monster in monsters:
            attack(obj, monster)


def attack(x, y):
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
