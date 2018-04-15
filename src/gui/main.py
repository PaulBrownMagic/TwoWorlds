from itertools import chain

import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from src.gui.config import FONT, COLOURS


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


def tile_colour(mp, world, fov, x, y):
    tile = "GROUND" if tcod.map_is_walkable(mp, x, y) else "WALL"
    return COLOURS[world][fov][tile]


def tile_char(mp, x, y):
    if tcod.map_is_walkable(mp, x, y):
        c = "." if tcod.map_is_transparent(mp, x, y) else "#"
    else:
        c = " "
    return c


def draw_map(mp, world):
    for tile in chain(*mp.tiles):
        x, y = tile.location
        if tcod.map_is_in_fov(mp, x, y):
            fov = "LIT"
            mp.tiles[y][x].explored = True
        else:
            fov = "DARK"
        if mp.tiles[y][x].explored:
            tcod.console_put_char_ex(con,
                                     x,
                                     y,
                                     tile_char(mp, x, y),
                                     (0, 0, 0),
                                     tile_colour(mp, world, fov, x, y))


def draw(item):
    tcod.console_put_char(con, item.location.x, item.location.y, item.char)
    tcod.console_set_char_foreground(con,
                                     item.location.x,
                                     item.location.y,
                                     item.colour)


def update_screen(level):
    draw_map(level.map_grid, level.world)
    draw(level.player)
    tcod.console_blit(src=con, x=0, y=0,
                      w=SCREEN_WIDTH, h=SCREEN_HEIGHT,
                      dst=root,
                      xdst=0, ydst=0)
    tcod.console_flush()
    tcod.console_clear(con)
