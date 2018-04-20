from random import randint, choice
from types import FunctionType

from tcod import color as colour

from src.maps.datatypes import Location
from src.objects.name_gen import name_generator


class Name:
    name: str
    realname: str

    def __init__(self, name, obj_type):
        randname = " ".join([name_generator.new()
                             for _ in range(randint(1, 3))])
        self.name = "a {} titled {}".format(obj_type, randname)
        self.realname = "a {} of {}".format(obj_type, name)

    def __str__(self):
        return self.name


class PotionName(Name):

    def __init__(self, name):
        super().__init__(name, "Potion")


class ScrollName(Name):

    def __init__(self, name):
        super().__init__(name, "Scroll")


class WandName:
    materials = ["Ebony", "Birch", "Mahogany", "Ash", "Beech", "Iron Wood",
                 "Redwood", "Silver", "Citrine", "Brass", "Honeysuckle",
                 "Amethyst", "Cherry", "Quartz", "Copper", "Lapis Lazuli",
                 "Maple", "Oak", "Surina", "Unikite"]

    def __init__(self, name):
        material = choice(WandName.materials)
        WandName.materials.remove(material)
        a_an = "An" if material[0] in "AEIOU" else "A"
        self.name = "{} {} Wand".format(a_an, material)
        self.realname = "Wand of {}".format(name)

    def __str__(self):
        return self.name


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


class AmuletOfYendor(Item):
    pass


class FunctioningItem(Item):
    function: FunctionType

    def __init__(self, name, char, colour, function):
        super().__init__(name, char, colour)
        self.function = function


class Scroll(FunctioningItem):
    used_up: bool = False


class Potion(FunctioningItem):
    pass


class Trap(FunctioningItem):
    pass


class Food(FunctioningItem):

    def __init__(self, name, char, colour, function, taste):
        super().__init__(name, char, colour, function)
        self.taste = taste


class Fruit(Food):
    pass


class Armour(Item):
    defence: int
    protected: bool = False

    def __init__(self, name, char, colour, defence):
        super().__init__(name, char, colour)
        self.defence = defence


def pos_neg(num):
    if num >= 0:
        return "+{}".format(num)
    else:
        return str(num)


class Weapon(Item):
    attack: str
    attack_mod: int
    dexterity_mod: int

    def __init__(self, name, char, colour, attack, attack_mod, dexterity_mod):
        super().__init__(name, char, colour)
        self.attack = attack
        self.attack_mod = attack_mod
        self.dexterity_mod = dexterity_mod

    @property
    def realname(self):
        return "[{}] [{}] {}".format(pos_neg(self.attack_mod),
                                     pos_neg(self.dexterity_mod),
                                     self.name)


class Projectile(Weapon):

    def __init__(self, name, char, colour, attack, thrown,
                 attack_mod, dexterity_mod):
        super().__init__(name, char, colour, attack, attack_mod, dexterity_mod)
        self.thrown = thrown  # attack when thrown
        self.weight = 0.01


class Monster(MovingObject):
    attack: str
    armour: int
    flags: str

    def __init__(self, name, char, colour,
                 state, attack, armour, hp, xp, flags, carry):
        super().__init__(name, char, colour, state, hp, xp)
        self.attack = attack
        self.armour = armour
        self.flags = flags
        self.carry = carry


class Player(MovingObject):
    max_strength: int
    xp_level: int = 1
    xp: int = 0
    inventory: dict = {l: None for l in "abcdefghijklmnopqrstuvwxyz"}
    wearing: Armour = None
    wielding: Weapon = None
    has_amulet_of_yendor: bool = False
    inventory_limit = 26
    hunger: int = 0
    # rings: [Rings] = []

    def __init__(self, armour, weapon, items):
        super().__init__("Rogue", "@", colour.white, "ACTIVE", 12, 0)
        self.strength = 16
        self.max_strength = self.strength
        self.wearing = armour
        self.wielding = weapon
        self.inventory['a'] = InventoryItem(armour)
        self.inventory['b'] = InventoryItem(weapon)
        for l, i in zip("cdefghijklmnopqrstuvwxyz", items):
            self.inventory[l] = InventoryItem(i)

    @property
    def xp_to_level_up(self):
        return 12*2**self.xp_level

    @property
    def attack(self):
        return self.wielding.attack if self.wielding is not None else "1d2"

    @property
    def armour(self):
        return self.wearing.defence if self.wearing is not None else 11


class MagicWand(FunctioningItem):

    def __init__(self, name, char, colour, function, count):
        super().__init__(name, char, colour, function)
        self.weight = 0.001
        self.count = count


class InventoryItem:
    count: int
    item: Item
    full: bool

    def __init__(self, item, count=1, max_count=1):
        self.item = item
        self.count = count
        self.max_count = max_count

    def __str__(self):
        return self.item

    @property
    def full(self):
        return self.count == self.max_count

    @property
    def weight(self):
        return self.count * self.item.weight
