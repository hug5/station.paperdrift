from flask import render_template


class HomeCtl:

    def __init__(self):
        pass

    def doStart(self):

        return render_template("homeHtml.j2")
        # return "<b>hello</b>"
