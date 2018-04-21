import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.gui.config import SKULL_FILE, CAKE_FILE, HUNGRY_FILE, TRAP_FILE
from src.gui.main import root
from src.config import vim


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError("Can't have more than 26 options in popup menu")
    fmt = "\n".join([header.center(width)+"\n"] +
                    options +
                    ["\n" + "--- press space to continue ---".center(width)])
    height = len(fmt.splitlines()) + 3
    popup = tcod.console_new(width, height)
    tcod.console_set_default_background(popup, (0, 0, 20))
    tcod.console_clear(popup)
    tcod.console_print_rect(popup, 1, 1, width+2, height+2, fmt=fmt)
    tcod.console_blit(src=popup, x=0, y=0,
                      w=width+2, h=height,
                      dst=root,
                      xdst=SCREEN_WIDTH//2-width//2,
                      ydst= 0, # SCREEN_HEIGHT//2-height//2,
                      ffade=1.0, bfade=0.8)
    tcod.console_flush()
    key = tcod.console_wait_for_keypress(flush=True)
    while key.c != 32:  # Space
        key = tcod.console_wait_for_keypress(flush=True)
    tcod.console_clear(popup)


def info_inv(level, item):
    if item == level.player.wearing:
        return "being worn"
    elif item == level.player.wielding:
        return "in hand"
    else:
        return ""


def cap(name, count):
    name = str(name)
    if count > 1 and not (name.endswith("Wand") or name.startswith("Wand")):
        name += "s"
    return name[0].upper() + name[1:]


def count(count):
    return "({}*) ".format(count) if count > 1 else ""


def inventory_menu(level):
    inv = level.player.inventory
    header = "Inventory"
    option = "{}) {}{} {}".format
    options = [option(l,
                      count(i.count),
                      cap(i.item.name, i.count),
                      info_inv(level, i.item))
               for l, i in inv.items() if i is not None]
    menu(header, options, 52)


def controls_menu(_):
    header = "Controls"
    option = "{}: {}".format
    options = [option(k, v.replace("_", " ").capitalize())
               for k, v in vim.items()]
    menu(header, options, 40)


def died_screen(level):
    width = 60
    if level.player.has_amulet_of_yendor:
        witham = "-- with the Amulet of Yendor"
    else:
        witham = ""
    header = "Game Over: You Died at Level: {}{}".format(level.number,
                                                         witham).center(width)
    with open(SKULL_FILE) as skull_file:
        # Adapted from: http://www.asciiworld.com/-Death-Co-.html
        skull_ascii = skull_file.readlines()
    menu(header, skull_ascii, width)


def win_screen():
    width = 60
    header = "You have retrieved the Amulet of Yendor."
    with open(CAKE_FILE) as cake_file:
        cake_ascii = cake_file.readlines()
    menu(header, cake_ascii, width)


def hungry_popup(msg):
    with open(HUNGRY_FILE) as hungry_file:
        hungry_ascii = hungry_file.readlines()
    menu(msg, hungry_ascii, 50)

def trap_popup(msg):
    with open(TRAP_FILE) as trap_file:
        menu(msg, trap_file.readlines(), 50)
