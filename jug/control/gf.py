# from flask import Flask
# from flask import flask
# import html
from markupsafe import Markup, escape
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


