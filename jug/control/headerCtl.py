from flask import render_template

class HeaderCtl():

    def __init__(self):
        self.html = ''
        pass

    def getHtml(self):
        return self.html

    def doHeader(self):
        self.html = render_template(
            "headerHtml.jinja",
        )

    def start(self):
        self.doHeader()

