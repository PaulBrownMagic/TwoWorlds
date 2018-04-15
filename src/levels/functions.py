from src.levels.datatypes import Level


def make_level(level_number, player):
    print("Making Level {}".format(level_number))
    return Level(level_number,
                 player,
                 [],
                 [])
