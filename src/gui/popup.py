import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.gui.main import root
from src.config import vim


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError("Can't have more than 26 options in popup menu")
    height = len(header.splitlines()) + len(options) + 3
    popup = tcod.console_new(width, height)
    fmt = "\n".join([header+"\n"] +
                    options +
                    ["\n---press space to continue---"])
    tcod.console_print_rect(popup, 0, 0, width, height, fmt=fmt)
    tcod.console_blit(src=popup, x=0, y=0,
                      w=width, h=height,
                      dst=root,
                      xdst=SCREEN_WIDTH//2-width//2,
                      ydst=SCREEN_HEIGHT//2-height//2,
                      ffade=1.0, bfade=0.8)
    tcod.console_flush()
    key = tcod.console_wait_for_keypress(flush=True)
    while key.c != 32:  # Space
        key = tcod.console_wait_for_keypress(flush=True)
    tcod.console_clear(popup)


def info_inv(level, item):
    if item == level.player.wearing:
        return "(wearing)"
    elif item == level.player.wielding:
        return "(wielding)"
    else:
        return ""


def inventory_menu(level):
    inv = level.player.inventory
    header = "Inventory"
    option = "{}) {} {}".format
    options = [option(l, i.name, info_inv(level, i))
               for l, i in inv.items() if i is not None]
    menu(header, options, 40)


def controls_menu(_):
    header = "Controls"
    option = "{}: {}".format
    options = [option(k, v.replace("_", " ").capitalize())
               for k, v in vim.items()]
    menu(header, options, 40)
