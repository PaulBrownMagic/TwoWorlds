from tcod.color import white

from src.levels import make_level
from src.maps import Location
from src.objects import Player


def play_level(level):
    pass


def play_game():
    player = Player(name="You",
                    location=Location(20, 20),
                    char="@",
                    colour=white,
                    state="ACTIVE",
                    attack=16,
                    defence=0,
                    hp=12,
                    )
    level_number = 1

    while not player.state == "DEAD":
        level = make_level(level_number)
        while not level.complete:
            play_level(level)
        level_number = level.number
