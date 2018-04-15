from src.maps.datatypes import Map
from src.objects.datatypes import (Item,
                                   MagicItem,
                                   Monster,
                                   MagicMonster)


class Level:
    map_grid: Map
    items: [Item]
    monsters: [Monster]
    number: int
    complete: bool = False

    def __init__(self, number, items, monsters):
        self.number = number
        self.map_grid = Map()
        self.items = items
        self.monsters = monsters


class MagicLevel(Level):
    items: [MagicItem]
    monsters: [MagicMonster]
