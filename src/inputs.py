import tcod

from src.gui import toggle_fullscreen


def handle_keys():
    user_input = get_user_input()
    if user_input == "FULLSCREEN":
        toggle_fullscreen()
    elif user_input == "ESCAPE":
        return "EXIT"
    return "PLAYING"


arrows = {15: "LEFT",
          16: "RIGHT",
          14: "UP",
          17: "DOWN"}

vim = {"h": "LEFT",
       "l": "RIGHT",
       "j": "DOWN",
       "k": "UP",
       "y": "UL",
       "u": "UR",
       "b": "DL",
       "n": "DR",
       ".": "WAIT"}


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
