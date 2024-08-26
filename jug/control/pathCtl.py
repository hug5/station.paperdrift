from flask import render_template
from ..lib import gLib


class PathCtl:

    def __init__(self, url):
        self.url = url.rstrip('/').capitalize()

    def doStart(self):

        import random

        def getPop():
            return gLib.getPop()

        def getAdj():
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
                "youthful",
                "abandoned",
                "windy",
                "rainy",
                "snowy",
                "humid",
                "putrid",
                "hilly"
            ]

            rnum = random.randint(0, len(adjectives_list)-1)
            return adjectives_list[rnum]

        def getPronoun():
            pronouns_list = [
                "hamlet",
                "village",
                "city",
                "town",
                "metropolis",
                "settlement",
                "borough",
                "colony",
                "district",
                "community"
            ]

            return pronouns_list[random.randint(0, len(pronouns_list)-1)]


        return render_template(
            "pathHtml.jinja",
            city = self.url,
            population = getPop(),
            adj = getAdj(),
            pronoun = getPronoun(),
        )
