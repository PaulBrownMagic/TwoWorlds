from functools import partial
from random import choice, randint

from src.levels.datatypes import Level, MagicLevel
from src.maps import place_in_room
from src.objects import Stairs
from src.objects.monsters import Bat, Emu


def make_level(level_number, player):
    stairs = Stairs()
    level = Level(level_number,
                  player,
                  stairs,
                  [],
                  [choice([Bat, Emu])() for _ in range(randint(4, 8))],
                  )
    place = partial(place_in_room, level.map_grid)
    place(stairs)
    list(map(place, level.monsters))
    return level
