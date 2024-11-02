from flask import render_template

class FooterCtl():

    def __init__(self):
        self.html = ''
        pass

    def getHtml(self):
        return self.html

    def doFooter(self):
        self.html = render_template(
            "footerHtml.jinja"
        )
