###
  # def Controller():

  #     jug = Flask(
  #         __name__,
  #         template_folder="jug/html"
  #     )


  #     @jug.route("/")
  #     def home():
  #         # return "<p>Hello3</p>"
  #         from jug.control import home
  #         return home.result


  #     @jug.route('/<path:url>')
  #     def pathUrl(url):
  #         return "<b>%s</b>" %url


  #     return jug


  # jug = Controller()


  # @jug.route("/<arg>")
  # def subpath(arg):
  #    return "<p>yahoo2 " + arg + "</p>"

  # @jug.route('/', defaults={'path1': ''})
  # if you also want to catch root; see URL Route Registrations

#------------------------------------------------------

# from flask import Flask, render_template
from flask import Flask, \
                  render_template, \
                  redirect

from jug.lib import gLib
from jug.control import pathCtl

# from ..control import home
# from ..control import gg
# import gf

class Router():

    def __init__(self):

        self.jug = Flask(
            __name__,
            template_folder="html"
        )

        self.article = ''
        self.header = ''
        self.footer = ''

        # self.pageHtml = ''


    def doCommon(self):
        # self.header = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"

        from jug.control import headerCtl

        obj = headerCtl.HeaderCtl()
        self.header = obj.doStart()


        # self.header = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
        self.footer = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"



    def doHome(self):

        # from jug.control import headerCtl

        # obj = headerCtl.HeaderCtl()
        # self.header = obj.doStart()

        self.doCommon()

        from jug.control import homeCtl

        obj = homeCtl.HomeCtl()
        self.article = obj.doStart()

        pageHtml = render_template(
            "pageHtml.jinja",
            header = self.header,
            article = self.article,
            footer = self.footer,
        )

        return gLib.stripJinjaWhiteSpace(pageHtml)


    def doSomePathUrl(self, url):

        self.doCommon()

        obj = pathCtl.PathCtl(url)
        self.article = obj.doStart()

        pageHtml = render_template(
            "pageHtml.jinja",
            header = self.header,
            article = self.article,
            footer = self.footer,
        )


        return gLib.stripJinjaWhiteSpace(pageHtml)


    def doRoute(self):

        # self.doCommon()

        @self.jug.route("/")
        def home():
            return self.doHome()


        @self.jug.route('/<path:url>')
        def somePathUrl(url):
            result = gLib.checkPathSlash(url)
            if result != True: return redirect(result, code=301)
            return self.doSomePathUrl(url)


    def doStart(self):
        self.doRoute()
        return self.jug




# from jug import router
# obj = Router()
# jug = obj.doStart()

# jug = Router()

jug = Router().doStart()
  # Can just shorten to 1 line like this;


# <style>
# @import url('https://fonts.googleapis.com/css2?family=Moderustic:wght@300..800&display=swap');
# </style>

# // <uniquifier>: Use a unique and descriptive class name
# // <weight>: Use a value from 300 to 800

# .moderustic-<uniquifier> {
#   font-family: "Moderustic", sans-serif;
#   font-optical-sizing: auto;
#   font-weight: <weight>;
#   font-style: normal;
# }

