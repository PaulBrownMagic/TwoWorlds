import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.gui.main import root
from src.config import vim


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError("Can't have more than 26 options in popup menu")
    height = len(header.splitlines()) + len(options) + 3
    popup = tcod.console_new(width, height)
    tcod.console_set_default_background(popup, (0, 0, 20))
    tcod.console_clear(popup)
    fmt = "\n".join([header.center(width)+"\n"] +
                    options +
                    ["\n" + "--- press space to continue ---".center(width)])
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
    return "[{}] ".format(count) if count > 1 else ""


def inventory_menu(level):
    inv = level.player.inventory
    header = "Inventory"
    option = "{}) {}{} {}".format
    options = [option(l,
                      count(i.count),
                      cap(i.item.name, i.count),
                      info_inv(level, i.item))
               for l, i in inv.items() if i is not None]
    menu(header, options, 42)


def controls_menu(_):
    header = "Controls"
    option = "{}: {}".format
    options = [option(k, v.replace("_", " ").capitalize())
               for k, v in vim.items()]
    menu(header, options, 40)
