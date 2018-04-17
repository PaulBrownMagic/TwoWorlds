from types import FunctionType

from tcod import color as colour

from src.maps.datatypes import Location


class Object:
    name: str
    location: Location
    char: str
    colour: colour.Color
    blocks: bool
    found: bool

    def __init__(self, name, char, colour):
        self.name = name
        self.char = char
        self.colour = colour
        self.blocks = False
        self.found = False


class Stairs(Object):

    def __init__(self):
        super().__init__("Stairs", "%", colour.darkest_green)


class MovingObject(Object):
    state: str
    xp: int
    hp: int
    max_hp: int

    def __init__(self, name, char, colour,
                 state, hp, xp):
        super().__init__(name, char, colour)
        self.state = state
        self.hp = hp
        self.max_hp = hp
        self.blocks = True
        self.xp = xp


class Item(Object):
    weight: int = 1
    picked_up = False


class FunctioningItem(Item):
    function: FunctionType
    realname: str  # name when identified

    def __init__(self, name, realname, char, colour, function):
        super().__init__(name, char, colour)
        self.function = function
        self.realname = realname


class Scroll(FunctioningItem):
    pass


class Armour(Item):
    defence: int

    def __init__(self, name, char, colour, defence):
        super().__init__(name, char, colour)
        self.defence = defence


class Weapon(Item):
    attack: int

    def __init__(self, name, char, colour, attack):
        super().__init__(name, char, colour)
        self.attack = attack


class Projectile(Weapon):

    def __init__(self, name, char, colour, attack, thrown):
        super().__init__(name, char, colour, attack)
        self.thrown = thrown  # attack when thrown


class Monster(MovingObject):
    attack: str
    armour: int
    flags: str

    def __init__(self, name, char, colour,
                 state, attack, armour, hp, xp, flags):
        super().__init__(name, char, colour, state, hp, xp)
        self.attack = attack
        self.armour = armour
        self.flags = flags


class Player(MovingObject):
    max_strength: int
    xp_level: int = 1
    xp: int = 0
    inventory: dict = {l: None for l in "abcdefghijklmnopqrstuvwxyz"}
    wearing: Armour = None
    wielding: Weapon = None
    has_amulet_of_yendor: bool = False
    # rings: [Rings] = []

    def __init__(self, armour, weapon):
        super().__init__("Rogue", "@", colour.white, "ACTIVE", 12, 0)
        self.strength = 16
        self.max_strength = self.strength
        self.wearing = armour
        self.wielding = weapon
        self.inventory['a'] = armour
        self.inventory['b'] = weapon

    @property
    def xp_to_level_up(self):
        return 10*2**self.xp_level

    @property
    def attack(self):
        return self.wielding.attack if self.wielding is not None else "1d2"

    @property
    def armour(self):
        return self.wearing.defence if self.wearing is not None else 11


class MagicMonster(Monster):
    pass


class MagicItem(FunctioningItem):
    pass


class MagicWand(Projectile):
    pass
