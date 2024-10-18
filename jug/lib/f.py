# from flask import Flask
# from flask import flask
# import html
# from flask import redirect
# from markupsafe import Markup, escape
from jug.lib.logger import logger

from markupsafe import escape
import random
import os

class F():

    @staticmethod
    def uwsgi_log(msg):

        # log_path = os.getcwd() + "/etc/log/uwsgi.log"
        log_path = os.getcwd() + "/etc/log/debug.log"
        # os.system("echo " + msg + " >> " + log_path)
        os.system(f"echo '--- {msg}' >> {log_path}")


    # escape("<script>alert(document.cookie);</script>")
    # Markup(u'&lt;script&gt;alert(document.cookie);&lt;/script&gt;')

    @staticmethod
    def checkPathSlash(url):
        # checks that url ends in slash

        # url2 = url.rstrip('/')  # right-strip;
            # This always makes sure there's no final slash;
        url2 = url.rstrip('/') + "/"
            # This makes usre there is always a final slash;
        if url2 != url:
            # return redirect('/' + url2, code=301)
            # return redirect('/' + url2, code=301)
                # The / makes the redirect at the root; otherwise, will just append the url;
            # return "here"
            # 301 /url2   # Not sure what this is about; doesn't seem to work;
            # if there's a / at url, then redirect to non-slash url;

            # raise redirect_to('/' + url2)

            return '/' + url2
            # return True

        return True

        # There doesn't seem to be a way to redirect directly from here; have to do a return; very lame!

    @staticmethod
    def stripJinja(html):
        # html = html.replace('\n', '').replace('   ', '').replace('  ', '')
        # # return html.replace('    ', '')
        # return html

        return ' '.join(html.split())
        # return ' '.join(html.split()).replace('> <', '><')
        # Split the string by white spaces and put into a list; then join back using ' ' (space)
        # Supposed to at most leave 1 white space;
        # Not perfect though; see white space between '> <', for instance;
        # Also note that we can use replace to make > < to ><,
        # but this will alter the css layout sometimes; This is a quandary;
        # I have not seen any noticeable difference between stripping (as I do above),
        # And not stripping; so maybe that's a good baseline to start with;

    @staticmethod
    def hesc(str):
        # result = flask.escape(str)
          # Not work
        # result = html.escape(str)
          # Works
        result = escape(str)
          # Works
        # return str
        return result

    @staticmethod
    def cd():
        import os
        cwd = os.getcwd()
        print(cwd)

    @staticmethod
    def getPop():
        # Get random population number

        # import math

        # random.seed()
        # num1 = 200 * random.random()
        # num2 = num1 * random.random()
        # num3 = num2 * random.random()
        # pop = num2 * num3 * num1
        # return math.ceil(pop)
        # return randrange(101, 100000)
          # Return a randomly selected element from range(start, stop, step).
        return f"{random.randint(1000, 8000000):,d}"
          # Return a random integer N such that a <= N <= b.
          # Alias for randrange(a, b+1).
          # Also add thousand separator;

    @staticmethod
    def getAdverb():
        adverbs_list = [
            "Turning",
            "Spinning",
            "Glowing",
            "Whirling",
            "Gyrating",
            "Pivotting",
            "Swiveling",
            "Twisting",
            "Rolling",
            "Smiling",
            "Grinning",
            "Stumbling",
            "Rolicking"
        ]

        rnum = random.randint(0, len(adverbs_list)-1)
        return adverbs_list[rnum]

    @staticmethod
    def getAdjective():
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

    @staticmethod
    def getPronoun():
        pronouns_list = [
            "backwater",
            "backwood",
            "banlieue",
            "boondocks",
            "borough",
            "city",
            "colony",
            "community",
            "district",
            "dukedom",
            "encampment",
            "enclave",
            "ghetto",
            "hamlet",
            "municipality",
            "outpost",
            "plantation",
            "settlement",
            "shtetl",
            "town",
            "village",
        ]

        return pronouns_list[random.randint(0, len(pronouns_list)-1)]

    @staticmethod
    def getFamousSyn():
        famous_list = [
            "famous",
            "infamous",
            "known",
            "distinguished",
            "notable",
            "celebrated",
            "distinguished",
            "prominent",
            "acclaimed",
            "respected",
            "maligned",
            "besmirched",
            "condemned",
            "vilified",
            "mocked",
            "ridiculed",
            "forgotten",
            "remembered",
            "disgraced"
        ]

        return famous_list[random.randrange(0, len(famous_list))]

    @staticmethod
    def getFamousFor():
        famous_list = [
            "ankle-breaking rocky hills",
            "smelly fishy lakes",
            "sinewy streams",
            "ham sandwich",
            "ungovernable men",
            "lonely women",
            "nosey grandmothers",
            "fat hamburger",
            "stinky fried rice",
            "green spaghetti",
            "pineapple pizza",
            "bean burritos",
            "seedy nightclubs",
            "fat trees",
            "nine seasons",
            "26 hour sun",
            "pretentious evenings",
            "gossipy citizens",
            "cranky temper",
            "greasy living",
            "feral dogs",
            "flying pigs",
            "lost diamonds",
            "absentee government",
            "quisling politicians",
            "fresh sparkling water",
            "antedeluvian architecture"
        ]

        return famous_list[random.randint(0, len(famous_list)-1)]
