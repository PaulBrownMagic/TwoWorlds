from itertools import chain
from functools import partial

import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from src.gui.config import FONT, COLOURS
from src.gui.panels import panel, update_panel
from src.maps.config import MAP_HEIGHT
from src.maps import same_location

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
            tile.explored = True
        else:
            fov = "DARK"
        if tile.explored:
            tcod.console_put_char_ex(con,
                                     x,
                                     y,
                                     tile_char(mp, x, y),
                                     tcod.color.black,
                                     tile_colour(mp, world, fov, x, y))


def blind_draw_map(level):
    remaining = int(level.player.state.split("_")[-1])
    remaining -= 1
    if remaining == 0:
        level.player.state = "ACTIVE"
    else:
        level.player.state = "BLIND_{}".format(remaining)
    for tile in chain(*level.map_grid.tiles):
        x, y = tile.location
        in_fov = tcod.map_is_in_fov(level.map_grid, x, y)
        if not in_fov:
            tile.explored = False
        elif same_location(level.player.location, tile.location):
            tile.explored = True
        if tile.explored:
            tcod.console_put_char_ex(con,
                                     x, y,
                                     tile_char(level.map_grid, x, y),
                                     tcod.color.black,
                                     tile_colour(level.map_grid, level.world,
                                                 "DARK", x, y)
                                     )


def draw_in_map(mp, item):
    in_fov = tcod.map_is_in_fov(mp, item.location.x, item.location.y)
    if ((in_fov or item.found) and not (hasattr(item, "flags") and
                                        "H" in item.flags)):
        _draw(item)


def draw_trap(trap):
    if trap.found:
        _draw(trap)


def _draw(item):
    tcod.console_put_char(con, item.location.x, item.location.y, item.char)
    tcod.console_set_char_foreground(con,
                                     item.location.x,
                                     item.location.y,
                                     item.colour)


def update_screen(level):
    draw = partial(draw_in_map, level.map_grid)
    if level.player.state.startswith("BLIND"):
        blind_draw_map(level)
    else:
        draw_map(level.map_grid, level.world)
        draw(level.stairs)
        list(map(draw_trap, level.traps))
        list(map(draw, level.items))
        list(map(draw, level.monsters))
    draw(level.player)
    update_panel(level)
    tcod.console_blit(src=con, x=0, y=0,
                      w=SCREEN_WIDTH, h=SCREEN_HEIGHT,
                      dst=root,
                      xdst=0, ydst=0)
    tcod.console_blit(src=panel, x=0, y=0,
                      w=SCREEN_WIDTH,
                      h=SCREEN_HEIGHT-MAP_HEIGHT,
                      dst=root,
                      xdst=0, ydst=MAP_HEIGHT)
    tcod.console_flush()
    tcod.console_clear(con)
    tcod.console_clear(panel)
