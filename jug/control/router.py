from jug.lib.logger import logger
  # need to import the logger variable;

from flask import Flask, \
                  render_template, \
                  redirect, \
                  request

from jug.dbo import dbc
from jug.lib import gLib


class Router():

    def __init__(self):

        dir_html = "../html"

        self.jug = Flask(
            __name__,
            # template_folder="jug/html"
            template_folder=dir_html,
        )

        self.jug.debug = True

        self.article = ''
        self.header = ''
        self.footer = ''

        self.logo = ''


    def doCommon(self):
        from jug.control import headerCtl
        from jug.control import footerCtl

        logger.info('DoCommon')

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
        # pass

    # def doDb(self):

        # try:

        #     # dbc = False
        #     dbo = dbc.Dbc()
        #     dbo.doConnect()

        #     # result = dbo.doQuery()[0][4]
        #     gLib.uwsgi_log("#1 query")
        #     result = dbo.doQuery()
        #     gLib.uwsgi_log("#2 query")
        #     result = dbo.doQuery()
        #     gLib.uwsgi_log("#3 query")
        #     result = dbo.doQuery()
        #     gLib.uwsgi_log("#4 query")
        #     result = dbo.doQuery()
        #     gLib.uwsgi_log("#5 query")
        #     result = dbo.doQuery()
        #     gLib.uwsgi_log("#6 query")
        #     result = dbo.doQuery()


        #     return result

        #     # return gLib.hesc(dbc)
        # except Exception as e:
        #     # print(f"Error committing transaction: {e}")
        #     return [["bad db connection", e]]
        # finally:
        #     dbo.doDisconnect()
        #     pass



    def doHome(self):
        from jug.control import homeCtl

        logger.info('DoHome')
        # gLib.uwsgi_log("doHome")

        # dbc = self.doDb()
        # gLib.uwsgi_log("post-dbc")

        self.doCommon()

        obj = homeCtl.HomeCtl()
        self.article = obj.doStart()

        pageHtml = render_template(
            "pageHtml.jinja",
            header = self.header,
            article = self.article,
            footer = self.footer,
            # db = dbc
        )

        return gLib.stripJinjaWhiteSpace(pageHtml) + self.logo


    def doSomePathUrl(self, url):
        from jug.control import pathCtl

        logger.info('DoSomePathUrl')

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

    def doCheckPath(self, url):

        # If url path is any of these, then go home;
        home_list = ["home", "paperdrift", "station paperdrift"]

        url = url.lower()

        # check for home or paperdrift in url; if so, go to root url;
        url2 = url.rstrip('/')
        if url2 in home_list: return "/"

        # check that url ends in /
        checkPath = gLib.checkPathSlash(url)
        if checkPath != True: return checkPath

        return True


    def doRoute(self):

        # self.doCommon()

        @self.jug.route("/")
        def home():

            # ip_addr = request.remote_addr

            # rpath = request.base_url
            # rpath = request.full_path
              # /foo/page.html?x=y
            rpath = request.url
              # http://www.example.com/myapplication/foo/page.html?x=y

            logger.info("URL " + rpath)

            return self.doHome()


        @self.jug.route('/<path:url>')
        def somePathUrl(url):

            # rpath = request.base_url

            # rpath = request.full_path
            rpath = request.url
            logger.info("URL " + rpath)

            # checkPath = gLib.checkPathSlash(url)
            # if checkPath != True: return redirect(checkPath, code=301)
              # Check for slash; If no ending / in url, then redirect to path with / suffix;
            checkPath = self.doCheckPath(url)
            if checkPath != True: return redirect(checkPath, code=301)

            return self.doSomePathUrl(url)

      # path             /foo/page.html
      # full_path        /foo/page.html?x=y
      # script_root      /myapplication

      # url_root         http://www.example.com/myapplication/
      # base_url         http://www.example.com/myapplication/foo/page.html
      # url              http://www.example.com/myapplication/foo/page.html?x=y


    def _start(self):

        self.doRoute()
        return self.jug



## These below don't work even when it appears to!
# method 1
# obj = Router()
# jug = obj._start()

# method 2
# jug = Router()._start()
  # Can just shorten to 1 line like this;

# These 2 may be equivalent and allows for debug mode
# $ flask --app hello run --debug
# app.run(debug=True)

# But how to do this on a running remote server running uwsgi?