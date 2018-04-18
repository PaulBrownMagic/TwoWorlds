from random import randint, choice

import tcod

from src.config import movements
# from src.inputs import movements, get_id_action
from src.maps import Location, is_blocked, is_walkable, same_location
from src.gui import message, update_screen, inventory_menu, controls_menu
from src.objects.datatypes import Player, Armour, Weapon, Projectile, Scroll
from src.objects.weapons import mace, make_weapon, weapons  # all_weapons
from src.objects.armour import ringmail, make_armour, armours
from src.objects.actions import actions

# flags: A: armour drain, M:mean, F:flying, H: hidden, R: regen hp,
# V: drain hp, X: drain xp, S:stationairy, L: lure player

move_ticker = 1


def run_move_logic(level, user_input):
    game_state = None
    if user_input in movements:
        tick_move(level)
        x, y = movements[user_input]
        _move(level.player, x, y, level)
        for monster in level.monsters:
            monster_move(level, monster)
        find_stairs(level)
        autopickup(level)
    elif user_input in actions:
        game_state = actions[user_input](level)
        print(game_state)
    return game_state if game_state is not None else "PLAYING"


def tick_move(level):
    global move_ticker
    move_ticker += 1
    if move_ticker % 20 == 0:
        for mon in filter(lambda m: "R" in m.flags, level.monsters):
            regen_health(mon, level.number)
        regen_health(level.player, level.number)


def do_hp_regen(level, mt):
    if level.number < 8:
        return mt % 21 - level.number * 2 == 0
    else:
        return mt % 3 == 0


def regen_health(mo, i):
    if i < 8:
        x = 1
    else:
        x = randint(1, i-7)
    mo.hp = mo.hp + x if mo.hp < mo.max_hp - x else mo.max_hp


def player_sleeping(level):
    player = level.player
    sleeping = False
    if player.state == "SLEEP":
        player.state = "ACTIVE"
        message("Rogue awakens")
    elif player.state.startswith("SLEEP"):
        message("Rogue sleeps")
        player.state = player.state[:-1]
        sleeping = True
    return sleeping


def is_confused(obj):
    confused = False
    if obj.state == "CONFUSED":
        obj.state = "ACTIVE"
        message("{} is no longer confused".format(obj.name.capitalize()))
    elif obj.state.startswith("CONFUSED"):
        obj.state = obj.state[:-1]
        confused = True
    return confused


def _move(obj, x, y, level, stationary=False):
    if type(obj) == Player and player_sleeping(level):
        return
    if is_confused(obj):
        x, y = movements[choice(list(movements))]
    new_location = Location(obj.location.x + x, obj.location.y + y)
    blocked = is_blocked(new_location, level)
    walkable = is_walkable(new_location, level)
    if walkable and not blocked and not stationary:
        obj.location = new_location
    if walkable and blocked:
        monsters = filter(lambda x: x.location == new_location and x.blocks,
                          level.monsters + [level.player])
        for monster in monsters:
            attack(obj, monster, level)


def find_stairs(level):
    in_fov = tcod.map_is_in_fov(level.map_grid, level.stairs.location.x,
                                level.stairs.location.y)
    if in_fov:
        level.stairs.found = True


def autopickup(level):
    itms = [item for item in level.items
            if same_location(level.player.location, item.location)]
    for itm in itms:
        pickup(level.player, itm)


def pickup(player, item):
    if same_location(player.location, item.location):
        spaces = [l for l, i in player.inventory.items() if i is None]
        if len(spaces) > 0:
            player.inventory[spaces[0]] = item
            item.picked_up = True
            message("Rogue picked up {}".format(item.name))
        else:
            message("Rogue's inventory is full")


def is_flying_targeting(monster):
    return "F" in monster.flags and \
            monster.state == "TARGETING" and \
            randint(1, 10) < 4


def monster_move(level, monster):
    update_monster_state(level, monster)
    stationary = "S" in monster.flags
    is_active = monster.state == "ACTIVE"
    is_confused = monster.state.startswith("CONFUSED")
    if is_active or is_confused or is_flying_targeting(monster):
        x, y = movements[choice(list(movements))]
        _move(monster, x, y, level, stationary)
    elif monster.state == "TARGETING":
        astar = tcod.path_new_using_map(level.map_grid, 1.95)
        tcod.path_compute(astar, monster.location.x, monster.location.y,
                          level.player.location.x, level.player.location.y)
        next_tile = tcod.path_get(astar, 0)
        x, y = (next_tile[0] - monster.location.x,
                next_tile[1] - monster.location.y)
        _move(monster, x, y, level, stationary)


def attack(x, y, level):
    if type(x) == type(y):
        return
    msg = "{} attacks {}".format(x.name, y.name)
    if does_attack_hit(x, y, level.number):
        y.hp -= damage_done_by(x)
        if y.hp <= 0:
            y.state = "DEAD"
            msg += " and defeats it."
            update_xp(x, y)
        else:
            msg += " and hits."
    else:
        msg += " and misses."
    message(msg)


def does_attack_hit(x, y, lvl_num):
    if type(x) == Player:
        if x.state == "CONFUSE_NEXT_MONSTER":
            y.state = "CONFUSED1234567890"
            x.state = "ACTIVE"
            message("{} looks confused".format(y.name.capitalize()))
        elif not y.state.startswith("CONFUSED"):
            y.state = "TARGETING"
        if x.strength < 7:
            mod = x.strength - 7
        elif x.strength > 23:
            mod = 3
        else:
            mod = (x.strength - 15)//2
        level = x.xp_level
        if "F" in y.flags:
            mod -= 3
    else:
        level = lvl_num
        mod = 0
        if "F" in x.flags:
            mod -= 3
    return randint(1, 20) + mod >= 20 - level - y.armour


def damage_done_by(x):
    mod = 0
    if type(x) == Player:
        if x.strength == 16:
            mod = 1
        elif x.strength == 17:
            mod = 2
        elif x.strength in [18, 19]:
            mod = 3
        elif x.strength in [20, 21]:
            mod = 4
        elif x.strength > 21:
            mod = 5
    return dice_roll(x.attack) + mod


def dice_roll(dice):
    count, sides = map(int, dice.split('d'))
    return sum([randint(1, sides) for _ in range(count)])


def update_xp(x, y):
    if type(x) == Player:
        x.xp += y.xp
        # Level Up
        if x.xp >= x.xp_to_level_up:
            x.xp_level += 1
            hp_up = dice_roll("3d5")
            x.hp += hp_up
            x.max_hp += hp_up
            message("Welcome to level {}".format(x.xp_level))


def update_monster_state(level, monster):
    in_fov = tcod.map_is_in_fov(level.map_grid,
                                monster.location.x, monster.location.y)
    if monster.hp <= 0:
        monster.state = "DEAD"
    elif in_fov and monster.state == "SNOOZING" and randint(1, 10) < 10:
        monster.state = "ACTIVE"
    elif in_fov and "M" in monster.flags and randint(1, 10) < 10:
        monster.state = "TARGETING"
    elif in_fov and monster.state == "ACTIVE" and randint(1, 10) < 8:
        monster.state = "TARGETING"


def make_player():
    return Player(weapon=make_weapon(mace),
                  armour=make_armour(ringmail)
                  )


def items_for(level):
    wpns = [make_weapon(choice(weapons)) for _ in range(randint(0, 3))]
    armrs = [make_armour(choice(armours)) for _ in range(randint(0, 3))]
    return wpns + armrs
