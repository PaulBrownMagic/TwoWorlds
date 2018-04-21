import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 52
TITLE = "Rogue: Through The Veil"

FOV_ALGO = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
FOV_RADIUS = 20

arrows = {15: "MOVE_LEFT",
          16: "MOVE_RIGHT",
          14: "MOVE_UP",
          17: "MOVE_DOWN",
          42: "MOVE_UP",
          36: "MOVE_DOWN",
          38: "MOVE_LEFT",
          40: "MOVE_RIGHT",
          41: "MOVE_UP_LEFT",
          43: "MOVE_UP_RIGHT",
          35: "MOVE_DOWN_LEFT",
          37: "MOVE_DOWN_RIGHT",
          39: "SEARCH",
          }

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
       "s": "SEARCH",
       "m": "MOVE_WITHOUT_PICKING_UP",
       ",": "PICK_UP_ITEM",
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

HUNGRY = 750
HUNGRY_WEAK = 850
step = 25
HUNGRY_FEINT = [HUNGRY_WEAK + x for x in range(step, 6*step, step)]
HUNGRY_DIE = HUNGRY_FEINT[-1] + 5
