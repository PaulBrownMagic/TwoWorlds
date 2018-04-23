import tcod

from src.config import movements, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO
from src.characters import (player_move,
                            actions,
                            player_surroundings,
                            monster_move,
                            regen_health,
                            add_monster)
from src.inputs import handle_keys
from src.gui import update_screen
from src.levels import update_level
from src.objects import underfoot


def play_level(level):
    tcod.map_compute_fov(level.map_grid,
                         level.player.location.x,
                         level.player.location.y,
                         radius=FOV_RADIUS - level.number//2,
                         light_walls=FOV_LIGHT_WALLS,
                         algo=FOV_ALGO)
    game_state = run_turn_logic(level,
                                run_move_logic(level,
                                               handle_keys(level)))
    update_level(level)
    update_screen(level)
    return game_state


move_ticker = 1


def run_move_logic(level, user_input):
    action = None
    if user_input in movements:
        player_move(level, movements[user_input])
    elif user_input in actions:
        action = actions[user_input](level)
    return user_input if action is None else action


def run_turn_logic(level, user_input):
    if user_input != "INVENTORY":
        trap = underfoot(level)
        # tick_move(level)
        for monster in level.monsters:
            if monster.state == "DEAD":
                # monster_drop(monster, level)
                pass
            else:
                monster_move(level, monster)
    if level.player.state == "DEAD":
        return "PLAYER_DEAD"
    else:
        return user_input if trap is None else trap


def tick_move(level):
    global move_ticker
    move_ticker += 1
    if move_ticker % 20 == 0:
        for mon in filter(monster_regens, level.monsters):
            regen_health(mon, level.number)
        regen_health(level.player, level.number)
    if move_ticker % 80 == 0:
        add_monster(level)
    if move_ticker % 20 == 0 and move_ticker % 80 == 0:
        move_ticker = 1
