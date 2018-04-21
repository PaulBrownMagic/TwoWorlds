from random import randint

import tcod

from src.gui import message
from src.objects.datatypes import (Player,
                                   Armour,
                                   Weapon,
                                   Projectile,
                                   Scroll,
                                   Monster)


def attack(x, y, level):
    if type(x) == type(y):
        return
    if does_attack_hit(x, y, level.number):
        dmg = damage_done_by(x)
        if type(x) == Monster:
            if "A" in x.flags:
                armour_drain(x, y)
            if "V" in x.flags:
                hp_drain(x, dmg)
            if "X" in x.flags:
                xp_drain(x, y)
            if "Z" in x.flags:
                str_drain(x, y)
        if type(y) == Monster:
            if "H" in y.flags:
                y.flags = y.flags.replace("H", "")
                print(y.flags)
        make_attack(x, y, dmg)
    else:
        message("{} attacks {} and misses".format(x.name, y.name))


def armour_drain(monster, player):
    if (randint(1, 2) == 1 and
            player.wearing is not None and
            not player.wearing.protected and
            "eather" not in player.wearing.name):
        player.wearing.defence += 1
        message("{} rusts your armour".format(monster.name))
    else:
        message("A strange liquid evapourates off your armour".format(monster.name))


def hp_drain(monster, dmg):
    monster.hp += dmg//2
    if monster.hp > monster.max_hp:
        monster.hp = monster.max_hp


def xp_drain(monster, player):
    player.xp -= 2*2**player.xp_level


def str_drain(monster, player):
    if randint(1, 3) == 3:
        message("Fighting {} drains your strength".format(monster.name))
        player.strength -= randint(1, 2)
        if player.strength < 0:
            player.strength = 0


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


def strength_mod(player, monster):
    if player.strength < 7:
        mod = player.strength - 7
    elif player.strength > 23:
        mod = 3
    else:
        mod = (player.strength - 15)//2
    return mod



def does_attack_hit(x, y, lvl_num, weapon=None):
    mod = 0
    if type(x) == Player:
        if weapon is None:
            weapon = x.wielding
        mod = weapon.dexterity_mod
        if x.state == "CONFUSE_NEXT_MONSTER":
            y.state = "CONFUSED1234567890"
            x.state = "ACTIVE"
            message("{} looks confused".format(y.name.capitalize()))
        elif not y.state.startswith("CONFUSED"):
            y.state = "TARGETING"
        mod += strength_mod(x, y)
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
    else:
        mod += int(x.attack.split('d')[0])
    return mod


def damage_done_by(x):
    if hasattr(x, "wielding"):
        weapon_mod = x.wielding.attack_mod
    else:
        weapon_mod = 0
    return dice_roll(x.attack) + mod_attack(x) + weapon_mod


def thrown_damage_done_by(itm, player):
    if hasattr(itm, "thrown"):
        dmg = dice_roll(itm.thrown) + itm.attack_mod
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
