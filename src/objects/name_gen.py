import random

# Code adapted from
# http://roguebasin.roguelikedevelopment.org/index.php?title=Markov_chains_name_generator_in_Python


# From https://www.behindthename.com/names/usage/norse-mythology
NAMES = ["Alfr", "Alvis", "Askr", "Baldr", "Borghild", "Brynhild", "Eir",
         "Embla", "Erna", "Freyja", "Freyr", "Frigg", "Gandralfr", "Gardr",
         "Gryd", "Grimhildr", "Kriemhild", "Gunther", "Groa", "Gudrun",
         "Gunnarr", "Heidrun", "Hel", "Huldr", "Idunn", "Jarl", "Leug",
         "Magni", "Nanp", "Njall", "Njordr", "Odinn", "Qrvar", "Saga",
         "Siv", "Signy", "Sigrun", "Sigurdr", "Sindri", "Skadi", "Skuld",
         "Svanhildr", "Porr", "Tyr", "Urdr", "Verdandi", "Vidarr",
         "Volundr", "Yngvi"]
###############################################################################
# Markov Name model
# A random name generator, by Peter Corbett
# http://www.pick.ucam.org/~ptc24/mchain.html
# This script is hereby entered into the public domain
###############################################################################
class Mdict:
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        else:
            raise KeyError(key)
    def add_key(self, prefix, suffix):
        if prefix in self.d:
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]
    def get_suffix(self,prefix):
        l = self[prefix]
        return random.choice(l)

class MName:
    """
    A name from a Markov chain
    """
    def __init__(self, chainlen = 2):
        """
        Building the dictionary
        """
        if chainlen > 10 or chainlen < 1:
            print("Chain length must be between 1 and 10, inclusive")
            sys.exit(0)

        self.mcd = Mdict()
        oldnames = []
        self.chainlen = chainlen

        for l in NAMES:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")

    def new(self):
        """
        New name from the Markov chain
        """
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if suffix == "\n" or len(name) > 9:
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.capitalize()


name_generator = MName()
