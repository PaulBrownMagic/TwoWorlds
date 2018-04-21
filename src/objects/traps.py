from random import choices, randint

from tcod import color as colour

from src.gui import trap_popup
from src.objects.datatypes import Trap
from src.objects.scrolls import (teleport,
                                 create_monster,
                                 aggravate_monsters,
                                 transition_worlds)
from src.objects.potions import confuse

T_COLOUR = colour.black


def poison_dart(level):
    level.player.hp -= randint(1, 3)
    trap_popup("A poison dart strikes Rogue")


def t_teleport(level):
    trap_popup("This tile gives you a strange feeling")
    teleport(level)


def t_confuse(level):
    confuse(level)
    trap_popup("You stumble on a trap and are confused")


def t_create_monster(level):
    create_monster(level)
    trap_popup("Is that a trap door?")


def t_aggravate_monsters(level):
    aggravate_monsters(level)
    trap_popup("That's a very squeaky tile to step on.")


def t_transition_worlds(level):
    trap_popup("You see some strange symbols on the ground")
    return transition_worlds(level)


traps = [dict(name="Teleportation", p=5, f=t_teleport),
         dict(name="Confusion", p=3, f=t_confuse),
         dict(name="Create Monster", p=2, f=t_create_monster),
         dict(name="Poison Dart", p=8, f=poison_dart),
         dict(name="Aggravate Monsters", p=3, f=t_aggravate_monsters),
         dict(name="Through The Veil", p=4, f=t_transition_worlds),
         ]


def make_trap(t):
    return Trap(name="{} Trap".format(t['name']),
                char="^",
                colour=T_COLOUR,
                function=t['f']
                )


def get_x_traps_for(num, level):
    allowed_traps = traps[1:] if level.world == "NORMAL" else traps
    weights = [t['p'] for t in allowed_traps]
    return list(map(make_trap, choices(allowed_traps, weights, k=num)))
