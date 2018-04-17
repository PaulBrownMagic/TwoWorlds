import tcod

from src.config import FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO
from src.gui import update_screen, message
from src.inputs import handle_keys
from src.levels import make_level, update_level
from src.maps import place_in_room
from src.objects import make_player


def play_level(level):
    game_state = handle_keys(level)
    update_level(level)
    tcod.map_compute_fov(level.map_grid,
                         level.player.location.x,
                         level.player.location.y,
                         radius=FOV_RADIUS,
                         light_walls=FOV_LIGHT_WALLS,
                         algo=FOV_ALGO)
    update_screen(level)
    return game_state


def setup_level(level_number, player):
    level = make_level(level_number, player)
    place_in_room(level.map_grid, player)
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
    level = setup_level(level_number, player)
    message("Welcome to Rogue: Through The Veil")
    message("Find the Amulet of Yendor and return it, but beware, \
            the magic realm is never far away.")
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
                    print("WON")
                    break
            else:
                level_number = level.number + 1
            level = setup_level(level_number, player)
            update_screen(level)
            game_state = "PLAYING"
        elif game_state == "PLAYER DEAD":
            print("GAME OVER")
            break
