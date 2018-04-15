from random import randint

from tcod import color as colour

from src.objects.datatypes import Monster
from src.maps import distance_to

M_COLOUR = colour.white

def choose_state(active, sleeping):
    roll = randint(1, 100)
    if roll <= active:
        return "ACTIVE"
    elif roll <= active + sleeping:
        return "SLEEPING"
    else:
        return "TARGETING"


def in_room_target(monster, level):
    if distance_to(monster.location, level.player.location) < 14:
        monster.state = "TARGETING"


class Bat(Monster):

    def __init__(self):
        super().__init__("Bat", "B", M_COLOUR,
                         choose_state(60, 35),
                         randint(1, 2),
                         randint(1, 3),
                         randint(2, 4),
                         1)
        self.targeting_condition = in_room_target

class Emu(Monster):

    def __init__(self):
        super().__init__("Emu", "E", M_COLOUR,
                       choose_state(50, 45),
                       randint(1, 2),
                       randint(1, 3),
                       randint(2, 4),
                       2)
        self.targeting_condition = in_room_target

