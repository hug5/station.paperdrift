from flask import render_template
from ..lib import gLib


class PathCtl:

    def __init__(self, url):
        self.url = url

    def doStart(self):

        pop = gLib.getPop()
        # moon = gLib.getMoon()
        headerHtml = render_template("headerHtml.j2")

        return render_template(
            "pathHtml.j2",
            path = self.url,
            population = pop,
            header = headerHtml
            # code = moon
        )
