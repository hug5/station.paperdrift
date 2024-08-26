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


class Router():

    def __init__(self):

        self.jug = Flask(
            __name__,
            template_folder="html"
        )

        self.article = ''
        self.header = ''
        self.footer = ''

        self.logo = ''


    def _start(self):
        self.doRoute()
        return self.jug


    def doCommon(self):
        from jug.control import headerCtl
        from jug.control import footerCtl

        def doHeader():
            obj = headerCtl.HeaderCtl()
            self.header = obj.doStart()

        def doFooter():
            obj = footerCtl.FooterCtl()
            self.footer = obj.doStart()

        def doLogo():
            self.logo = render_template(
                "logo.jinja"
            )

        doHeader()
        doFooter()
        doLogo()


    def doHome(self):
        from jug.control import homeCtl

        self.doCommon()

        obj = homeCtl.HomeCtl()
        self.article = obj.doStart()

        pageHtml = render_template(
            "pageHtml.jinja",
            header = self.header,
            article = self.article,
            footer = self.footer,
        )

        return gLib.stripJinjaWhiteSpace(pageHtml) + self.logo


    def doSomePathUrl(self, url):
        from jug.control import pathCtl

        self.doCommon()

        obj = pathCtl.PathCtl(url)
        self.article = obj.doStart()

        pageHtml = render_template(
            "pageHtml.jinja",
            header = self.header,
            article = self.article,
            footer = self.footer,
        )

        return gLib.stripJinjaWhiteSpace(pageHtml) + self.logo


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




# method 1
# obj = Router()
# jug = obj._start()

# method 2
jug = Router()._start()
  # Can just shorten to 1 line like this;


