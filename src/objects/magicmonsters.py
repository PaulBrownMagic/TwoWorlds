SL = "SLEEPING"
SN = "SNOOZING"
A = "ACTIVE"
STATES = [SL, SN, A]

# flags: A: armour drain, M: mean, F: flying, H: hidden, R: regen hp,
# V: drain hp, X: drain xp, S: stationairy, L: lure player

a = dict(name="Aquator", levels=(8, 17), carry=0, flags="A", xp=20, ac=2,
         hp="5d8", dmg="1d1", state=A)
b = dict(name="Banshee", levels=(19, 999), carry=0, flags="", xp=100, ac=7,
         hp="7d8", dmg="3d4", state=A)
c = dict(name="Centaur", levels=(7, 16), carry=15, flags="", xp=25, ac=4,
         hp="4d8", dmg="1d6", state=SN)
d = dict(name="Dragon", levels=(22, 999), carry=100, flags="M", xp=6800, ac=-1,
         hp="10d8", dmg="3d10", state=SN)
e = dict(name="Enfield", levels=(1, 7), carry=0, flags="", xp=2, ac=7,
         hp="1d8", dmg="1d4", state=SN)
f = dict(name="Fairy", levels=(1, 11), carry=0, flags="MF", xp=1, ac=8,
         hp="1d8", dmg="1d3", state=A)
g = dict(name="Griffin", levels=(17, 999), carry=20, flags="MFR", xp=2000,
         ac=2, hp="13d8", dmg="3d5", state=SN)
i = dict(name="Imp", levels=(1, 10), carry=0, flags="", xp=15, ac=9,
         hp="1d8", dmg="1d2", state=A)
h = dict(name="Hobgoblin", levels=(1, 9), carry=10, flags="M", xp=3, ac=5,
         hp="1d8", dmg="1d8", state=SN)
j = dict(name="Jabberwock", levels=(21, 999), carry=70, flags="", xp=4000,
         ac=6, hp="15d8", dmg="2d12", state=SN)
k = dict(name="Korrigan", levels=(1, 6), carry=33, flags="M", xp=1, ac=7,
         hp="1d8", dmg="1d4", state=A)
l = dict(name="Ladon", levels=(14, 23), carry=70, flags="", xp=80, ac=3,
         hp="8d8", dmg="3d6", state=SL)
m = dict(name="Mandrake", levels=(18, 999), carry=0, flags="", xp=200, ac=2,
         hp="6d8", dmg="4d5", state=SL)
n = dict(name="Nidhogg", levels=(10, 19), carry=100, flags="M", xp=37, ac=9,
         hp="3d8", dmg="3d6", state=SN)
o = dict(name="Orc", levels=(3, 12), carry=15, flags="", xp=5, ac=6,
         hp="1d8", dmg="1d8", state=A)
p = dict(name="Pegasus", levels=(15, 24), carry=50, flags="FR", xp=120, ac=2,
         hp="8d8", dmg="4d4", state=SN)
q = dict(name="Quagga", levels=(9, 18), carry=0, flags="M", xp=32, ac=2,
         hp="3d8", dmg="1d4", state=SN)
r = dict(name="Rå", levels=(4, 13), carry=80, flags="HR", xp=35, ac=8,
         hp="2d8", dmg="1d6", state=SL)
s = dict(name="Siren", levels=(6, 15), carry=0, flags="SL", xp=10, ac=8,
         hp="3d8", dmg="2d4", state=SL)
t = dict(name="Troll", levels=(12, 21), carry=15, flags="RM", xp=120, ac=4,
         hp="6d8", dmg="2d6", state=A)
u = dict(name="Urvile", levels=(16, 25), carry=0, flags="M", xp=190, ac=-1,
         hp="7d8", dmg="4d6", state=SN)
v = dict(name="Vampire", levels=(20, 999), carry=20, flags="VRM", xp=350,
         ac=1, hp="8d8", dmg="1d10", state=SN)
w = dict(name="Wraith", levels=(13, 22), carry=0, flags="X", xp=55, ac=4,
         hp="5d8", dmg="1d6", state=A)
x = dict(name="Xiao", levels=(1, 8), carry=0, flags="FM", xp=1, ac=3,
         hp="1d8", dmg="1d2", state=A)
y = dict(name="Yeti", levels=(11, 20), carry=30, flags="", xp=50, ac=6,
         hp="4d8", dmg="1d6", state=SN)
z = dict(name="Zombie", levels=(3, 14), carry=0, flags="M", xp=6, ac=8,
         hp="2d8", dmg="1d8", state=A)

magic_monsters = [a, b, c, d, e, f, g, h, i, j, k, l, m,
                  n, o, p, q, r, s, t, u, v, w, x, y, z]
