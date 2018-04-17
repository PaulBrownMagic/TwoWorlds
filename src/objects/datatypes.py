from types import FunctionType

from tcod import color

from src.maps.datatypes import Location


class Object:
    name: str
    location: Location
    char: str
    colour: color.Color
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
        super().__init__("Stairs", "%", color.darkest_green)


class MovingObject(Object):
    state: str
    attack: str
    strength: int
    armour: int
    xp: int
    hp: int
    max_hp: int

    def __init__(self, name, char, colour,
                 state, attack, armour, hp, xp,
                 strength=0):
        super().__init__(name, char, colour)
        self.state = state
        self.attack = attack
        self.armour = armour
        self.hp = hp
        self.max_hp = hp
        self.blocks = True
        self.xp = xp
        self.strength = strength


class Item(Object):
    weight: int = 1


class FunctioningItem(Item):
    function: FunctionType

    def __init__(self, name, char, colour, function):
        super().__init__(name, char, colour)
        self.function = function


class Armour(Item):
    defence: int

    def __init__(self, name, char, colour, defence):
        super().__init__(name, char, colour)
        self.defence = defence


class Weapon(Item):
    attack: int
    precision: int

    def __init__(self, name, char, colour, attack, precision):
        super().__init__(name, char, colour)
        self.attack = attack
        self.precision = precision


class Projectile(Weapon, FunctioningItem):

    def __init__(self, name, char, colour, attack, precision):
        super().__init__(name, char, colour, attack, precision)
        self.function = None  # Must write


class Monster(MovingObject):
    flags: str

    def __init__(self, name, char, colour,
                 state, attack, armour, hp, xp, flags):
        super().__init__(name, char, colour, state, attack, armour, hp, xp)
        self.flags = flags


class Player(MovingObject):
    max_strength: int
    xp_level: int = 1
    xp: int = 0
    carrying_weight_limit: int = 14
    inventory: list = []
    wearing: Armour = None
    weilding: Weapon = None
    has_amulet_of_yendor: bool = False
    # rings: [Rings] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_strength = self.strength

    @property
    def xp_to_level_up(self):
        return 10*self.xp_level + 2**self.xp_level



class MagicMonster(Monster):
    pass


class MagicItem(FunctioningItem):
    pass


class MagicWand(Projectile):
    pass
