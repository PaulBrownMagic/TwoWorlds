import os

from tcod.color import Color

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
FONT = os.path.join(ASSETS_DIR, "dejavu10x10_gs_tc.png")

N_DARK_WALL = Color(31, 31, 16)
N_LIT_WALL = Color(130, 103, 23)
N_DARK_GROUND = Color(41, 41, 22)
N_LIT_GROUND = Color(173, 138, 31)

M_DARK_WALL = Color(31, 10, 10)
M_LIT_WALL = Color(71, 0, 0)
M_DARK_GROUND = Color(41, 10, 10)
M_LIT_GROUND = Color(97, 0, 0)

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
