# Rogue: Through The Veil

Rogue: Through The Veil is yet another roguelike. In this twist on the
classic game, you are constrained to a dungeon of your normal, everyday
monsters and items. However, just beyond the veil there exists a magical
world where incredible creatures roam and mystical items await
discovery. During your search for the Amulet of Yendor, you will
discover how to go beyond the veil, transitioning between the realms of
reality and the magical. You will be able to bring magical items back to
the real world to aid you in your quest, but beware, the magical world
is a dangerous place.

## Requirements

This game is written in Python3, although only tested withprint(key) Python3.6,
features specific to Python3.6 have been avoided, so it should run with
earlier versions.

Requirements can be installed with pip, the use of a virtualenv is
recommended:

```
pip install -r requirements.txt
```

If you are on a Linux machine you may also need to install libsdl2 for
tcod:

```
sudo apt install libsdl2-dev
```

## How To Run Game

With requirements installed, you can run:

```
python run.py
```

## Basic Controls

You can move your character, "@", using the VI/VIM keys, or for those too cool
for that, you can also use the arrow keys. It's recommended that you either use
the VI/VIM keys or a numpad (with NumLock off) so you can move diagonally.

Walk into a monster to melee attack it. Press "t" to throw something at it. View
all the controls with "?", and if you're being asked what item you'd like to use
and can't remember, press "\*".

## How To Win

The objective is to go down through the dungeons until you find the
Amulet Of Yendor, which starts appearing at level 26. From there you go back
up though the levels to reach the surface, only then do you win the game.

## Difficulty

The game *should* be very difficult to actually win, I've known people play
Rogue for decades without ever winning it. My PB in Rogue is being killed on
Level 26 with the Amulet. If I've balanced this game right, it'll be about the
same. **Good Luck!**
