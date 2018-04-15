import tcod

from src.gui import update_screen
from src.inputs import handle_keys
from src.levels import make_level
from src.maps import Location, place_in_room
from src.objects import Player


def play_level(level):
    game_state = handle_keys(level)
    update_screen(level)
    return game_state


def play_game():
    player = Player(name="You",
                    location=Location(20, 20),
                    char="@",
                    colour=tcod.color.white,
                    state="ACTIVE",
                    attack=16,
                    defence=0,
                    hp=12,
                    )
    level_number = 1
    level = make_level(level_number, player)
    place_in_room(level.map_grid, player)
    update_screen(level)

    while not tcod.console_is_window_closed():
        game_state = play_level(level)
        if game_state == "EXIT":
            break
        elif game_state == "NEXT_LEVEL":
            level_number = level.number
            level = make_level(level_number)
            place_in_room(level.map_grid, player)
        elif game_state == "PLAYER DEAD":
            print("GAME OVER")
            break
