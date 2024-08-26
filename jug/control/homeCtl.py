from flask import render_template
from jug.lib import gLib

class HomeCtl():

    def __init__(self):
        pass


    def doHome(self):

        pop = gLib.getPop()
        # moon = gLib.getMoon()
        # headerHtml = render_template("headerHtml.jinja")

        return render_template(
            "homeHtml.jinja",
            population=pop,
            # header = headerHtml
            # code=moon
        )
        # return "<b>hello</b>"


    def doStart(self):
        return self.doHome()

