# from flask import Flask
# from flask import flask
# import html
# from flask import redirect
from markupsafe import Markup, escape
import random
import os


def uwsgi_log(msg):

    log_path = os.getcwd() + "/etc/log/uwsgi.log"
    # os.system("echo " + msg + " >> " + log_path)
    os.system(f"echo {msg} >> {log_path}")


# escape("<script>alert(document.cookie);</script>")
# Markup(u'&lt;script&gt;alert(document.cookie);&lt;/script&gt;')

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
    else:
        return True

    # There doesn't seem to be a way to redirect directly from here; have to do a return; very lame!

def stripJinjaWhiteSpace(pageHtml):
    # pageHtml = pageHtml.replace('\n', '').replace('   ', '').replace('  ', '')
    # # return pageHtml.replace('    ', '')
    # return pageHtml

    return ' '.join(pageHtml.split())
    # Split the string by white spaces and put into a list; then join back using ' ' (space)
    # Supposed to at most leave 1 white space;
    # Not perfect though; see white space between '> <', for instance;
    # Not sure about speed between this and doing replace command;

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
    return f"{random.randint(101, 500000):,d}"
      # Return a random integer N such that a <= N <= b.
      # Alias for randrange(a, b+1).
      # Also add thousand separator;


def getMoon():
    moonArr = ['◐', '◑', '◒', '◓', '◔', '◕']
    # return moonArr[random.randrange(0, 6)]
    return random.choice(moonArr)
      # Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
