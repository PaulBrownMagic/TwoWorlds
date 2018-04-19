from tcod import color as colour

from src.objects.datatypes import AmuletOfYendor


amulet = AmuletOfYendor(name="The Amulet of Yendor",
                        char="'",
                        colour=colour.red,
                        )


def get_amulet():
    return amulet


def is_amulet(itm):
    return type(itm) == AmuletOfYendor
