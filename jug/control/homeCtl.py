from flask import render_template
from ..lib import gLib

class HomeCtl:

    def __init__(self):
        pass

    def doStart(self):

        pop = gLib.getPop()
        # moon = gLib.getMoon()
        # headerHtml = render_template("headerHtml.j2")

        return render_template(
            "homeHtml.j2",
            population=pop,
            # header = headerHtml
            # code=moon
        )
        # return "<b>hello</b>"
