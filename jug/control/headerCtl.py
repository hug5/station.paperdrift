from flask import render_template
from jug.lib.g import G

class HeaderCtl():

    def __init__(self):
        self.html = ''
        pass

    def getHtml(self):
        return self.html

    def doHeader(self):
        # baseUrl = G.site["baseUrl"]
        baseUrl = "/"
        self.html = render_template(
            "headerHtml.jinja",
            baseUrl = baseUrl
        )

    def start(self):
        self.doHeader()

