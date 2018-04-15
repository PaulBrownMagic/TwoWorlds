from tcod.color import Color

from src.config import SCREEN_WIDTH


MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = 45

MIN_ROOM_W = 4
MAX_ROOM_W = 14
MIN_ROOM_H = 2
MAX_ROOM_H = 10


N_DARK_WALL = Color(41, 41, 10)
N_LIT_WALL = Color(51, 51, 0)
N_DARK_GROUND = Color(51, 51, 10)
N_LIT_GROUND = Color(77, 77, 0)

M_DARK_WALL = Color(41, 10, 10)
M_LIT_WALL = Color(51, 0, 0)
M_DARK_GROUND = Color(51, 10, 10)
M_LIT_GROUND = Color(77, 0, 0)

COLOURS = {"NORMAL": {"DARK": {"WALL": N_DARK_WALL,
                               "GROUND": N_DARK_GROUND},
                      "LIT": {"WALL": N_LIT_WALL,
                              "GROUND": N_LIT_GROUND}
                      },
           "MAGIC": {"DARK": {"WALL": M_DARK_WALL,
                              "GROUND": M_DARK_GROUND},
                     "LIT": {"WALL": M_LIT_WALL,
                             "GROUND": M_LIT_GROUND}
                     }
           }
