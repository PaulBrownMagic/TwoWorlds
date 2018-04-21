from itertools import chain
from functools import partial
from random import choice

import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from src.gui.config import FONT, COLOURS
from src.gui.panels import panel, update_panel, message
from src.maps.config import MAP_HEIGHT
from src.maps import same_location, is_walkable, is_blocked, is_transparent, Location, in_fov

tcod.console_set_custom_font(FONT,
                             tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GRAYSCALE)

con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
root = tcod.console_init_root(SCREEN_WIDTH,
                              SCREEN_HEIGHT,
                              title=TITLE,
                              fullscreen=False
                              )


def toggle_fullscreen():
    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


def tile_colour(level, fov, loc):
    tile = "GROUND" if is_walkable(loc, level) else "WALL"
    return COLOURS[level.world][fov][tile]


def tile_char(level, loc):
    if is_walkable(loc, level):
        c = "." if is_transparent(loc, level) else "#"
    else:
        c = " "
    return c


def draw_map(level):
    for tile in chain(*level.map_grid.tiles):
        if in_fov(tile.location, level):
            fov = "LIT"
            tile.explored = True
        else:
            fov = "DARK"
        if tile.explored:
            tcod.console_put_char_ex(con,
                                     tile.location.x,
                                     tile.location.y,
                                     tile_char(level, tile.location),
                                     tcod.color.black,
                                     tile_colour(level, fov, tile.location))


def decr_state(player):
    state, remaining = player.state.split("_")
    remaining = int(remaining)
    remaining -= 1
    if remaining == 0:
        player.state = "ACTIVE"
        message("Everything returns to normal")
    else:
        player.state = "{}_{}".format(state, remaining)


def blind_draw_map(level):
    for tile in chain(*level.map_grid.tiles):
        if not in_fov(tile.location, level):
            tile.explored = False
        elif same_location(level.player.location, tile.location):
            tile.explored = True
        if tile.explored:
            tcod.console_put_char_ex(con,
                                     tile.location.x, tile.location.y,
                                     tile_char(level, tile.location),
                                     tcod.color.black,
                                     tile_colour(level, "DARK", tile.location)
                                     )


def draw_in_map(draw_func, level, item):
    if ((in_fov(item.location, level) or item.found) and
            not (hasattr(item, "flags") and "H" in item.flags)):
        draw_func(item)


def draw_trap(trap):
    if trap.found:
        _draw(trap)


def _draw(item):
    tcod.console_put_char(con, item.location.x, item.location.y, item.char)
    tcod.console_set_char_foreground(con,
                                     item.location.x,
                                     item.location.y,
                                     item.colour)


def h_draw(item):
    items = "/%:'?!])"
    monsters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if item.char in items:
        char = choice(items)
    elif item.char in monsters:
        char = choice(monsters)
    else:
        char = item.char
    colour = choice([tcod.color.white, tcod.color.red, tcod.color.blue,
                     tcod.color.green, tcod.color.amber, tcod.color.azure,
                     tcod.color.brass, tcod.color.celadon, tcod.color.copper,
                     tcod.color.chartreuse, tcod.color.crimson, tcod.color.cyan,
                     tcod.color.fuchsia, tcod.color.han, tcod.color.flame,
                     tcod.color.gold, tcod.color.lime, tcod.color.magenta,
                     tcod.color.orange, tcod.color.peach, tcod.color.pink,
                     tcod.color.purple, tcod.color.sea, tcod.color.turquoise,
                     tcod.color.violet, tcod.color.yellow])
    tcod.console_put_char(con, item.location.x, item.location.y, char)
    tcod.console_set_char_foreground(con,
                                     item.location.x,
                                     item.location.y,
                                     colour)


def update_screen(level):
    if level.player.state.startswith("HALLUCINATE"):
        draw = partial(draw_in_map, h_draw, level)
        decr_state(level.player)
    else:
        draw = partial(draw_in_map, _draw, level)
    if level.player.state.startswith("BLIND"):
        blind_draw_map(level)
        decr_state(level.player)
    else:
        draw_map(level)
        draw(level.stairs)
        list(map(draw_trap, level.traps))
        list(map(draw, level.items))
        list(map(draw, level.monsters))
    draw(level.player)
    update_panel(level)
    tcod.console_blit(src=con, x=0, y=0,
                      w=SCREEN_WIDTH, h=SCREEN_HEIGHT,
                      dst=root,
                      xdst=SCREEN_WIDTH//8, ydst=0)
    tcod.console_blit(src=panel, x=0, y=0,
                      w=SCREEN_WIDTH,
                      h=SCREEN_HEIGHT-MAP_HEIGHT,
                      dst=root,
                      xdst=0, ydst=MAP_HEIGHT)
    tcod.console_flush()
    tcod.console_clear(con)
    tcod.console_clear(panel)
