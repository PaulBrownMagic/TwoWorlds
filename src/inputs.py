import tcod

from src.config import arrows, vim
from src.gui import toggle_fullscreen
from src.maps import same_location
from src.objects import run_move_logic


def handle_keys(level):
    user_input = get_user_input()
    if user_input == "FULLSCREEN":
        toggle_fullscreen()
    elif user_input == "ESCAPE":
        return "EXIT"
    elif (user_input == "TAKE_STAIRS_DOWN" and
          not level.player.has_amulet_of_yendor and
          same_location(level.player.location, level.stairs.location)):
        return "NEXT_LEVEL"
    elif (user_input == "TAKE_STAIRS_UP" and
          level.player.has_amulet_of_yendor and
          same_location(level.player.location, level.stairs.location)):
        return "NEXT_LEVEL"
    run_move_logic(level, user_input)
    return "PLAYING"

def get_user_input():
    key = tcod.console_wait_for_keypress(flush=False)
    if key.vk in arrows:
        return arrows[key.vk]
    elif key.vk == 66 and key.text in vim:
        return vim[key.text]
    elif key.vk == 1:
        return "ESCAPE"
    elif key.vk == 4 and (key.lalt or key.ralt):
        return "FULLSCREEN"
