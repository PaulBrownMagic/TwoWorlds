from src.maps import Location, is_blocked, is_walkable, same_location

movements = {"UP": (0, -1),
             "DOWN": (0, 1),
             "LEFT": (-1, 0),
             "RIGHT": (1, 0),
             "UR": (1, -1),
             "UL": (-1, -1),
             "DL": (-1, 1),
             "DR": (1, 1),
             "WAIT": (0, 0),
             }


def run_move_logic(level, user_input):
    if user_input in movements:
        x, y = movements[user_input]
        _move(level.player, x, y, level)


def _move(obj, x, y, level):
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    if walkable and not blocked:
        obj.location = new_location
