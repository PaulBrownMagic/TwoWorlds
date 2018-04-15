from src.levels.datatypes import Level, MagicLevel
from src.maps import place_in_room
from src.objects import Stairs


def make_level(level_number, player):
    stairs = Stairs()
    level = Level(level_number,
                  player,
                  stairs,
                  [],
                  [])
    place_in_room(level.map_grid, stairs)
    return level
