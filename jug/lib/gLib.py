# from flask import Flask
# from flask import flask
# import html
from markupsafe import Markup, escape
import random

# escape("<script>alert(document.cookie);</script>")
# Markup(u'&lt;script&gt;alert(document.cookie);&lt;/script&gt;')


def hesc(str):
    # result = flask.escape(str)
      # Not work
    # result = html.escape(str)
      # Works
    result = escape(str)
      # Works
    # return str
    return result


def cd():
    import os

    cwd = os.getcwd()
    print(cwd)


def getPop():

    # import math

    # random.seed()
    # num1 = 200 * random.random()
    # num2 = num1 * random.random()
    # num3 = num2 * random.random()
    # pop = num2 * num3 * num1
    # return math.ceil(pop)
    # return randrange(101, 100000)
      # Return a randomly selected element from range(start, stop, step).
    return random.randint(101, 100000)
      # Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1).


def getMoon():
    moonArr = ['◐', '◑', '◒', '◓', '◔', '◕']
    # return moonArr[random.randrange(0, 6)]
    return random.choice(moonArr)
      # Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
