import tcod

from src.config import arrows, vim
from src.gui import toggle_fullscreen, message, update_screen, inventory_menu
from src.maps import same_location


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
    return user_input


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


def get_id_action(level):
    message("--- (* to view inventory)")
    update_screen(level)
    key = tcod.console_wait_for_keypress(flush=True)
    while key.vk not in [66, 1]:
        key = tcod.console_wait_for_keypress(flush=False)
    if key.text == "*":
        inventory_menu(level)
        return get_id_action(level)
    if key.text in level.player.inventory:
        return key.text
    else:
        message("Unknown item")
        return None


def is_direction_key(key):
    is_arrow_key = key.vk in list(arrows)
    is_vim_key = key.vk == 66 and key.text in "hjklyubn"
    return is_arrow_key or is_vim_key


def get_dir_action(level):
    message("direction?")
    update_screen(level)
    key = tcod.console_wait_for_keypress(flush=False)
    while not is_direction_key(key):
        if key.vk == 1:  # ESC
            return None
        key = tcod.console_wait_for_keypress(flush=False)
    if key.vk in arrows:
        return arrows[key.vk]
    elif key.vk == 66 and key.text in "hjklyubn":
        return vim[key.text]
    else:
        return None
