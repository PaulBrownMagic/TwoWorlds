from src.maps import in_fov, same_location


def underfoot(level):
    find_stairs(level)
    return triggertrap(level)


def find_stairs(level):
    if in_fov(level.stairs.location, level):
        level.stairs.found = True


def triggertrap(level):
    traps = (trap for trap in level.traps
             if same_location(level.player.location, trap.location))
    for trap in traps:
        trap.found = True
        return trap.function(level)
