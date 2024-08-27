from flask import render_template
from ..lib import gLib
import random


class PathCtl:

    def __init__(self, url):
        # self.url = url.rstrip('/').capitalize()
        self.url = url.rstrip('/').title()

    def getPop(self):
        return gLib.getPop()

    def getAdjective(self):
        adjectives_list = [
            "beautiful",
            "bucolic",
            "decrepit",
            "dilapidated",
            "perilous",
            "friendly",
            "tax-free",
            "high-crime",
            "sinking",
            "modern",
            "floating",
            "callow",
            "guilty",
            "unkempt",
            "maniculred",
            "abandoned",
            "fashionable",
            "gastronomic",
            "landlocked",
            "windy",
            "rainy",
            "snowy",
            "humid",
            "putrid",
            "hilly"
        ]

        rnum = random.randint(0, len(adjectives_list)-1)
        return adjectives_list[rnum]

    def getPronoun(self):
        pronouns_list = [
            "hamlet",
            "outpost",
            "village",
            "city",
            "town",
            "banlieue",
            "settlement",
            "borough",
            "colony",
            "district",
            "ghetto",
            "backwoods",
            "community"
        ]

        return pronouns_list[random.randint(0, len(pronouns_list)-1)]

    def getFamousFor(self):
        famous_list = [
            "rocky hills",
            "fishy lakes",
            "sinewy streams",
            "ham sandwich",
            "obstreperous men",
            "curious women",
            "fat hamburger",
            "stinky fried rice",
            "green spaghetti",
            "pineapple pizza",
            "bean burrito",
            "seedy nightclubs",
            "long trees",
            "nine seasons",
            "24 hour sun",
            "pretentious evenings",
            "gossipy citizens",
            "cranky temper",
            "greasy living",
            "feral dogs",
            "lost diamonds",
            "efficient government",
            "quisling politicians",
            "fresh water",
            "antedeluvian architecture"
        ]

        return famous_list[random.randint(0, len(famous_list)-1)]


    def doPath(self):

        return render_template(
            "pathHtml.jinja",
            city = self.url,
            population = self.getPop(),
            adj = self.getAdjective(),
            famous = self.getFamousFor(),
            pronoun = self.getPronoun(),
        )

    def doStart(self):
        return self.doPath()

