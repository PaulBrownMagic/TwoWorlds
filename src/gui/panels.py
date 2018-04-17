from itertools import repeat

import tcod

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.maps.config import MAP_HEIGHT

messages = []

panel = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT-MAP_HEIGHT)


def message(msg):
    messages.append(msg)
    while len(messages) > 4:
        del messages[0]


def render_bar(x, y, total_width, name, value, maximum, bar_colour, bg_colour):
    bar_width = int(value/maximum * total_width)
    txt = "{}: {}/{}".format(name, value, maximum)
    for i, (char, col) in enumerate(zip(txt.center(total_width),
                                        list(repeat(bar_colour, bar_width)) +
                                        list(repeat(bg_colour,
                                                    total_width-bar_width)))):
        tcod.console_put_char_ex(panel, x + i, y, char, tcod.color.white, col)


def render_hp_bar(player):
    render_bar(1, 1, 20,
               "HP", player.hp, player.max_hp,
               tcod.color.red, tcod.color.darkest_red)


def render_str_bar(player):
    render_bar(1, 2, 20,
               "Str", player.strength, player.max_strength,
               tcod.color.blue, tcod.color.darkest_blue)


def render_messages():
    tcod.console_print_rect(panel, 22, 0,
                            SCREEN_WIDTH - 22, SCREEN_HEIGHT-MAP_HEIGHT-4,
                            fmt="\n".join(messages))


def update_panel(level):
    tcod.console_print(panel, 1, 0, "Level: {}".format(level.number))
    render_hp_bar(level.player)
    render_str_bar(level.player)
    arm = 11 - level.player.armour
    tcod.console_print(panel, 1, 3,
                       "XP: {}|{}   Arm: {}".format(level.player.xp_level,
                                                    level.player.xp,
                                                    arm)
                       )
    render_messages()
