import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 52
TITLE = "Rogue: Beyond The Veil"

FOV_ALGO = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
FOV_RADIUS = 16

arrows = {15: "MOVE_LEFT",
          16: "MOVE_RIGHT",
          14: "MOVE_UP",
          17: "MOVE_DOWN"}

vim = {"h": "MOVE_LEFT",
       "l": "MOVE_RIGHT",
       "j": "MOVE_DOWN",
       "k": "MOVE_UP",
       "y": "MOVE_UP_LEFT",
       "u": "MOVE_UP_RIGHT",
       "b": "MOVE_DOWN_LEFT",
       "n": "MOVE_DOWN_RIGHT",
       ".": "WAIT",
       ">": "TAKE_STAIRS_DOWN",
       "<": "TAKE_STAIRS_UP",
       "T": "TAKE_OFF_ARMOUR",
       "W": "WEAR_ARMOUR",
       "w": "WIELD_WEAPON",
       "d": "DROP_ITEM",
       "r": "READ_SCROLL",
       "q": "QUAFF_POTION",
       "t": "THROW_ITEM",
       "z": "ZAP_WAND",
       "i": "INVENTORY",
       "e": "EAT",
       "?": "VIEW_CONTROLS",
       }

movements = {"MOVE_UP": (0, -1),
             "MOVE_DOWN": (0, 1),
             "MOVE_LEFT": (-1, 0),
             "MOVE_RIGHT": (1, 0),
             "MOVE_UP_RIGHT": (1, -1),
             "MOVE_UP_LEFT": (-1, -1),
             "MOVE_DOWN_LEFT": (-1, 1),
             "MOVE_DOWN_RIGHT": (1, 1),
             "WAIT": (0, 0),
             }

HUNGRY = 1000
HUNGRY_WEAK = 1500
step = 20
HUNGRY_FEINT = [HUNGRY_WEAK + x for x in range(0, 5*step, step)]
HUNGRY_DIE = HUNGRY_FEINT[-1] + 5
