from random import choice, choices, randint

import tcod

from src.maps import place_in_room
from src.characters.combat import mod_attack, make_attack, dice_roll
from src.objects.datatypes import WandName, MagicWand
from src.characters.datatypes import Monster
from src.characters.monsters import monsters, make_monster


W_COLOUR = tcod.color.white


def needs_target(func):
    """Optional decorator @needs_target, skipping for more fun!"""
    def func_wrapper(level, target):
        if type(target) == Monster:
            func(level, target)
    return func_wrapper


def lightning(level, target):
    dmg = dice_roll("6d6") + mod_attack(level.player)
    make_attack(level.player, target, dmg)


def hide(level, target):
    """Incomplete"""
    target.flags += "H"


def polymorph(level, target):
    location = target.location
    new_monster = make_monster(choice(monsters[level.world]))
    new_monster.location = location
    new_monster.state = "ACTIVE"
    level.monsters.remove(target)
    level.monsters.append(new_monster)


def magic_missile(level, target):
    dmg = dice_roll("1d4") + mod_attack(level.player)
    make_attack(level.player, target, dmg)


def drain_life(level, target):
    dmg = level.player.hp//2
    make_attack(level.player, target, dmg)
    make_attack(target, level.player, dmg)


def nothing(level, target):
    """Do Nothing!"""
    pass


def teleport_away(level, target):
    place_in_room(level, target)


def create_monster(level, target):
    monster = make_monster(choice(monsters_for(level)))
    monster.state = "TARGETING"
    monster.location = level.player.location
    for _ in range(5):
        if monster.location == level.player.location:
            x, y = movements[choice(list(movements))]
            _move(monster, x, y, level)
        else:
            level.monsters.append(monster)
            message("A {} appeared".format(monster.name))
            return


def cancellation(level, target):
    target.flags = ""


def vampiric(level, target):
    dmg = dice_roll("1d4") + mod_attack(level.player)
    make_attack(level.player, target, dmg)
    level.player.hp += dmg
    if level.player.hp >= level.player.max_hp:
        level.player.max_hp += 1
        level.player.hp = level.player.max_hp


Name = WandName

wands = [
    dict(name=Name("Lightning"), p=9, f=lightning),
    dict(name=Name("Hiding"), p=5, f=hide),
    dict(name=Name("Polymorph"), p=12, f=polymorph),
    dict(name=Name("Magic Missile"), p=10, f=magic_missile),
    dict(name=Name("Vampiric Regeneration"), p=5, f=vampiric),
    dict(name=Name("Drain Life"), p=9, f=drain_life),
    dict(name=Name("Nothing"), p=1, f=nothing),
    dict(name=Name("Teleport Away"), p=6, f=teleport_away),
    dict(name=Name("Summoning"), p=6, f=create_monster),
    dict(name=Name("Cancellation"), p=5, f=cancellation),
]


def make_wand(w):
    return MagicWand(
        name=w['name'],
        char="/",
        colour=W_COLOUR,
        function=w['f'],
        count=randint(2, 10)
    )


def get_x_wands(num):
    weights = [w['p'] for w in wands]
    return list(map(make_wand, choices(wands, weights, k=num)))
