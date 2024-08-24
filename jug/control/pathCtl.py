from flask import render_template
from ..lib import gLib


class PathCtl:

    def __init__(self, url):
        self.url = url.rstrip('/').capitalize()

    def doStart(self):

        pop = gLib.getPop()
        # moon = gLib.getMoon()
        headerHtml = render_template("headerHtml.jinja")

        return render_template(
            "pathHtml.jinja",
            path = self.url,
            population = pop,
            header = headerHtml
            # code = moon
        )
