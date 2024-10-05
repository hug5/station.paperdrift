from jug.lib.logger import logger
  # need to import the logger variable;

from flask import Flask, \
                  render_template, \
                  redirect, \
                  request

# from jug.dbo import dbc
from jug.lib import gLib

from jug.control.g import G
from pathlib import Path
import tomli


# import json
# from json import dumps
# from werkzeug.routing import Request
# from werkzeug.wrappers import Request, Response
# from werkzeug.test import create_environ


class RouterCtl():

    def __init__(self):

        dir_html = "../html"

        self.jug = Flask(
            __name__,
            # template_folder="jug/html"
            template_folder=dir_html,
        )

        # self.jug.debug = True

        self.article = ''
        self.header = ''
        self.footer = ''
        self.logo = ''

        self.doAdmin_toml()

    def doAdmin_toml(self):
        try:

            admin_toml_path = Path("jug/conf/admin.toml")
            if not Path(admin_toml_path).is_file():
                raise FileNotFoundError(f"File Not Found: {admin_toml_path}.")

            with admin_toml_path.open(mode='rb') as file_toml:
                admin_toml = tomli.load(file_toml)
                # If bad, should give FileNotFoundError

            G["weatherAPI_key"] = admin_toml["weatherAPI"]["key"]
            G["db"]["un"] = admin_toml["db"]["un"]
            G["db"]["pw"] = admin_toml["db"]["pw"]
            G["db"]["host"] = admin_toml["db"]["host"]
            G["db"]["port"] = admin_toml["db"]["port"]
            G["db"]["database"] = admin_toml["db"]["database"]

        except FileNotFoundError as e:
            logger.exception(f"admin.toml Load Error: {e}")
        except Exception as e:
            logger.exception(f"doAdmin_toml Error: {e}")
        finally:
            logger.info(f'weatherAPI_key: {G["weatherAPI_key"]}')



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

        homeO = homeCtl.HomeCtl()
        self.article = homeO.doStart()

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

        # Doing this for aesthetic; don't want a path that is /home, /paperdrift or /station paperdrift
        # Also check that all paths end with trailing slash;

        checkPath = ''
          # Dilemma: don't want to make this variable global;
          # But also want to be able to use within local functions below;
          # So declare here; and assign as nonlocal within local functions?

        def check_path_url():
            # Check for certain paths we ant to avoid; assign to home if so;

            nonlocal url  # avoid unbound variable error;

            # If url path is any of these, then go home;
            home_list = ["home", "paperdrift", "station paperdrift"]
            url = url.lower()

            # check for home or paperdrift in url; if so, go to root url;
            url2 = url.rstrip('/')
            # if url2 in home_list: return "/"
            if url2 in home_list:
                return True
            # Otherwise should return false implicitly


        def check_trailing_slash():
            # Check there is trailing slash in paths;
            nonlocal url
            nonlocal checkPath

            # check that url ends in /
            checkPath = gLib.checkPathSlash(url)
            # if checkPath != True: return checkPath
            if not checkPath:
                return checkPath
            # Otherwise should return false implicitly


        if check_path_url():
            return "/"
        if check_trailing_slash():
            return checkPath

        return True

    def doRequestUrl(self):


        # Assume this url:
        # https://station.paperdrift.com/something/?a=b


        rpath = request.url_root
        logger.info("---URL url_root: " + rpath)
          # https://station.paperdrift.com/

        rpath = request.base_url
        logger.info("---URL base_url: " + rpath)
            # https://station.paperdrift.com/something/

        rpath = request.url
        logger.info("---URL url: " + rpath)
          # https://station.paperdrift.com/something/?a=b

        rpath = request.full_path
        logger.info("---URL full_path: " + rpath)
          # /something/?a=b
          # /?   # will always have a ? on the index or other page ERRONESOUSLY;

        rpath = request.environ['PATH_INFO']
        logger.info("---URL PATH_INFO: " + rpath)
            # /something/

        rpath = request.environ['QUERY_STRING']
        logger.info("---URL QUERY_STRING: " + rpath)
          # a=b

        # These below give me the same IP address
        # rpath = request.remote_addr
        # logger.info("---Remote Address: " + rpath)
          # 84.239.5.141
        rpath = request.environ['REMOTE_ADDR']
        logger.info("---Remote Address2: " + rpath)
          # 84.239.5.141


        # This gives us the TRUE RAW uri; ? and // are always shown
        rpath = request.environ["REQUEST_URI"]
        logger.info("---uri: " + rpath)
          # /something/?a=b

        # print everything; check uwsgi_log
        # print(request.environ)

        # Also:
        # logger.debug, logger.info, logger.warning, logger.error, logger.critical


    def checkTrailingQuestion(self):

        # check for /?/ and /??+ path (2 or more question marks);
        ch_qmark = request.full_path
        if ch_qmark == "/?/" or ch_qmark.find("/??") >= 0 :
            return False # Not okay; redirect

        return True # okay


    def doRoute(self):

        # self.doCommon()
        @self.jug.before_request
        def before_request_route():
            # Shared logic to log the request before processing
            # print(f"Request received: {request.method} {request.url}")
            logger.info("---route_common Yay!")
            # logger.error("---UH")
            self.doRequestUrl()
            # if self.checkTrailingQuestion() == False:
            if not self.checkTrailingQuestion():
                rpath = request.base_url
                return redirect(rpath, code=301)


        @self.jug.route("/")
        def home():
            logger.info("---in home")
            return self.doHome()



        @self.jug.route('/<path:url>')
        def somePathUrl(url):

            # self.doRequestUrl()
            # self.checkTrailingQuestion()

            # checkPath = gLib.checkPathSlash(url)
            # if checkPath != True: return redirect(checkPath, code=301)
              # Check for slash; If no ending / in url, then redirect to path with / suffix;
            checkPath = self.doCheckPath(url)
            # if checkPath != True: return redirect(checkPath, code=301)
            if not checkPath:
                return redirect(checkPath, code=301)

            return self.doSomePathUrl(url)

      # path             /foo/page.html
      # full_path        /foo/page.html?x=y
      # script_root      /myapplication

      # url_root         http://www.example.com/myapplication/
      # base_url         http://www.example.com/myapplication/foo/page.html
      # url              http://www.example.com/myapplication/foo/page.html?x=y


    def start(self):

        self.doRoute()
        return self.jug



## These below don't work even when it appears to!
# method 1
# obj = Router()
# jug = obj.start()

# method 2
# jug = Router().start()
  # Can just shorten to 1 line like this;

# These 2 may be equivalent and allows for debug mode
# $ flask --app hello run --debug
# app.run(debug=True)

# But how to do this on a running remote server running uwsgi?

