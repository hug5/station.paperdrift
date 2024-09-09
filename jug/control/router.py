import logging
logger = logging.getLogger(__name__)
# logging.basicConfig(filename='etc/log/debug.log', level=logging.DEBUG)
logging.basicConfig(
    filename='etc/log/debug.log',
    encoding="utf-8",        # I'm getting a warning message?
    filemode="a",            # a is default
    level=logging.DEBUG,
    format="[{levelname}] {message} {module}:{lineno} ({asctime})",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logger.info('Started')

from flask import Flask, \
                  render_template, \
                  redirect

from jug.dbo import dbc
from jug.lib import gLib


class Router():

    def __init__(self):



        # import os

        # os.chdir("../html")
        # print("xxxxxxxxxxxxxxxxxxxxxxxxxx")
        # print(os.getcwd())
        # os.chdir("/home/h5/DATA/zData/Coding/Projects/webdev/station.paperdrift/jug")
        # print(os.getcwd())
        # dir_html = os.getcwd() + "/jug/html"
        dir_html = "../html"

        self.jug = Flask(
            __name__,
            # template_folder="jug/html"
            template_folder=dir_html
        )

        # self.jug.debug = True

        self.article = ''
        self.header = ''
        self.footer = ''

        self.logo = ''


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

        gLib.uwsgi_log("doHome")

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
            return self.doHome()


        @self.jug.route('/<path:url>')
        def somePathUrl(url):
            # checkPath = gLib.checkPathSlash(url)
            # if checkPath != True: return redirect(checkPath, code=301)
              # Check for slash; If no ending / in url, then redirect to path with / suffix;
            checkPath = self.doCheckPath(url)
            if checkPath != True: return redirect(checkPath, code=301)

            return self.doSomePathUrl(url)



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


