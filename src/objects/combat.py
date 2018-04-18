from random import randint

import tcod

from src.gui import message
from src.objects.datatypes import Player, Armour, Weapon, Projectile, Scroll


def attack(x, y, level):
    if type(x) == type(y):
        return
    if does_attack_hit(x, y, level.number):
        make_attack(x, y, damage_done_by(x))
    else:
        message("{} attacks {} and misses".format(x.name, y.name))


def make_attack(x, y, dmg):
    msg = "{} attacks {}".format(x.name, y.name)
    y.hp -= dmg
    if y.hp <= 0:
        y.state = "DEAD"
        msg += " and defeats it."
        update_xp(x, y)
    else:
        msg += " and hits."
    message(msg)


def does_attack_hit(x, y, lvl_num):
    if type(x) == Player:
        if x.state == "CONFUSE_NEXT_MONSTER":
            y.state = "CONFUSED1234567890"
            x.state = "ACTIVE"
            message("{} looks confused".format(y.name.capitalize()))
        elif not y.state.startswith("CONFUSED"):
            y.state = "TARGETING"
        if x.strength < 7:
            mod = x.strength - 7
        elif x.strength > 23:
            mod = 3
        else:
            mod = (x.strength - 15)//2
        level = x.xp_level
        if "F" in y.flags:
            mod -= 3
    else:
        level = lvl_num
        mod = 0
        if "F" in x.flags:
            mod -= 3
    return randint(1, 20) + mod >= 20 - level - y.armour


def mod_attack(x):
    mod = 0
    if type(x) == Player:
        if x.strength == 16:
            mod = 1
        elif x.strength == 17:
            mod = 2
        elif x.strength in [18, 19]:
            mod = 3
        elif x.strength in [20, 21]:
            mod = 4
        elif x.strength > 21:
            mod = 5
    return mod


def damage_done_by(x):
    return dice_roll(x.attack) + mod_attack(x)


def thrown_damage_done_by(itm, player):
    if hasattr(itm, "thrown"):
        dmg = dice_roll(itm.thrown)
        if player.wielding.name == "Short Bow" and itm.name == "Arrow":
            dmg += 2
    else:
        dmg = randint(1, 3)
    return dmg + mod_attack(player)


def dice_roll(dice):
    count, sides = map(int, dice.split('d'))
    return sum([randint(1, sides) for _ in range(count)])


def update_xp(x, y):
    if type(x) == Player:
        x.xp += y.xp
        # Level Up
        if x.xp >= x.xp_to_level_up:
            x.xp_level += 1
            hp_up = dice_roll("3d5")
            x.hp += hp_up
            x.max_hp += hp_up
            message("Welcome to level {}".format(x.xp_level))
