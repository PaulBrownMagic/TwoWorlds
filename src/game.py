import tcod

from src.config import FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO
from src.gui import update_screen, message, died_screen, win_screen
from src.inputs import handle_keys
from src.levels import make_level, update_level
from src.maps import place_in_room
from src.characters import make_player
from src.run_logic import play_level


def setup_level(world, level_number, player):
    level = make_level(world, level_number, player)
    place_in_room(level, player)
    tcod.map_compute_fov(level.map_grid,
                         player.location.x,
                         player.location.y,
                         radius=FOV_RADIUS,
                         light_walls=FOV_LIGHT_WALLS,
                         algo=FOV_ALGO)
    return level


def play_game():
    player = make_player()
    level_number = 1
    level = setup_level("NORMAL", level_number, player)
    message("Welcome to Rogue: Through The Veil")
    message("Find the Amulet of Yendor and return it, but beware, the magic realm is never far away.\n")
    message("--- (? to view controls)")
    update_screen(level)

    while not tcod.console_is_window_closed():
        game_state = play_level(level)
        if game_state == "EXIT":
            break
        elif game_state == "NEXT_LEVEL":
            if level.player.has_amulet_of_yendor:
                level_number = level.number - 1
                if level_number == 0:
                    game_state = "WON"
                    break
            else:
                level_number += 1
            level = setup_level("NORMAL", level_number, player)
            update_screen(level)
            game_state = "PLAYING"
        elif game_state == "TOGGLE_WORLDS":
            world = "MAGIC" if level.world == "NORMAL" else "NORMAL"
            if level.world == "MAGIC":
                level_number += 1
            level = setup_level(world, level_number, player)
            update_screen(level)
            game_state = "PLAYING"
        elif game_state == "PLAYER_DEAD":
            break
    if game_state == "EXIT":
        print("Thanks for playing! Come back soon, we have cake.")
    elif game_state == "WON":
        win_screen()
        print("Congratulations, I suppose.")
    elif game_state == "PLAYER_DEAD":
        died_screen(level)
        print("Oops, you died. Better luck next time.")
