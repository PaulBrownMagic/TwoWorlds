from random import choices, randint

from tcod import color as colour

from src.gui import message
from src.objects.datatypes import Trap
from src.objects.scrolls import (teleport,
                                 create_monster,
                                 aggravate_monsters,
                                 transition_worlds)
from src.objects.potions import confuse

T_COLOUR = colour.black


def poison_dart(level):
    message("A poison dart strikes Rogue")
    level.player.hp -= randint(1, 3)


traps = [dict(name="Teleportation", p=5, f=teleport),
         dict(name="Confusion", p=3, f=confuse),
         dict(name="Create Monster", p=2, f=create_monster),
         dict(name="Poison Dart", p=8, f=poison_dart),
         dict(name="Aggravate Monsters", p=3, f=aggravate_monsters),
         dict(name="Through The Veil", p=4, f=transition_worlds),
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
