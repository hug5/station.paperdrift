from flask import render_template


class PathCtl:

    def __init__(self, url):
        self.url = url

    def doStart(self):

        return render_template("pathHtml.j2",
                               path=self.url
        )
        # return "<b>hello</b>"
