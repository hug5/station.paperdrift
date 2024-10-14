from jug.lib.logger import logger
  # need to import the logger variable

                  # render_template, \
                  # g as G
from flask import Flask, \
                  redirect, \
                  request

# from jug.dbo import dbc
from jug.lib.f import F
from jug.lib.g import G
from pathlib import Path
import tomli
import re

from jug.control.pageCtl import PageCtl


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
        self.doConfig_toml()

        self.router_result = False
        self.redirect = [False, '']

        # G.get_db()
        # G.get_api()
        # G.get_site()


    def getRouter_result(self):
        return self.router_result

    def doConfig_toml(self):

        try:
            config_toml_path = Path("jug/conf/config.toml")
            if not Path(config_toml_path).is_file():
                raise FileNotFoundError(f"File Not Found: {config_toml_path}.")

            with config_toml_path.open(mode='rb') as file_toml:
                config_toml = tomli.load(file_toml)
                # If bad, should give FileNotFoundError

            G.api["weatherAPI_key"] = config_toml.get("api", {}).get("weatherAPI_key")

            G.db["un"] = config_toml["db"]["un"]
            G.db["pw"] = config_toml["db"]["pw"]
            G.db["host"] = config_toml["db"]["host"]
            G.db["port"] = config_toml["db"]["port"]
            G.db["database"] = config_toml["db"]["database"]

            G.site["name"] = config_toml["site"]["name"]
            G.site["tagline"] = config_toml["site"]["tagline"]

        except FileNotFoundError as e:
            logger.exception(f"config.toml Load Error: {e}")
        except Exception as e:
            logger.exception(f"doConfig_toml Error: {e}")
        finally:
            # logger.info(f'weatherAPI_key: {G["weatherAPI_key"]}')
            logger.info(f'weatherAPI_key: {G.api["weatherAPI_key"]}')


    def doCheckBadPath(self, url):

        # Doing this for aesthetic; don't want a path that is /home, /paperdrift or /station paperdrift
        # Also check that all paths end with trailing slash;

        # checkPath = ''
          # Dilemma: don't want to make this variable global;
          # But also want to be able to use within local functions below;
          # So declare here; and assign as nonlocal within local functions?

        def check_path_url():
            # Check for certain paths we ant to avoid; assign to home if so;

            # nonlocal url  # avoid unbound variable error;

            # If url path is any of these, then go home;
            home_list = ["home", "paperdrift", "station paperdrift"]
            url2 = url.lower()


            # check for home or paperdrift in url; if so, go to root url;
            url3 = url2.rstrip('/')
            # if url3 in home_list: return "/"
            if url3 in home_list:
                logger.info("---redirecting to /")
                return "/"
            return None


        def check_trailing_slash():
            # Check there is trailing slash in paths;
            # nonlocal checkPath
            # nonlocal url

            # check that url ends in /
            checkPath = F.checkPathSlash(url)
            # if checkPath != True: return checkPath
            # if not checkPath:
            if checkPath:
                return checkPath
            return None

        def cleanUrl():
            # nonlocal url
            url2 = url.rstrip('/')

            # remove non-alphanumeric characters, but allow for space
            # all bad characters will be replaced with space;
            # then later we'll remove redundant spaces;
            new_url = re.sub(r'[^a-zA-Z0-9\- ]', ' ', url2)
            # new_url2 = new_url.replace("  ", " ")
            # new_url = new_url.replace("%20%%20", "x")
            # new_url = new_url.replace("%20", "x")
            # new_url = new_url.replace("20%", "x")
            # new_url = new_url.replace("%", "x")
              # This doesn't seem to work right... always some edge problem;
              # When you ahve a weird url like this:
              # https://station.paperdrift.com/busan%20%20%20%%20%20korea/
              # I think the server crashes before it even gets here;
              # Weird... not the %20 isn't showing up!

            # remove redundant spaces
            new_url2 = ' '.join(new_url.split())

            # Don't need to escape since we removed all bad characters;
            # escaped_url = F.hesc(new_url)

            if new_url2 != url2:
                logger.info(f'Cleaned url: {new_url2} : {url2}')
                return "/" + new_url2 + "/"
            # else:
            #     # logger.info(f'good url: {escaped_url}')
            #     logger.info(f'Good url: {new_url2}')
            return None

            # clean_text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
            # print(clean_text)


        # if check_trailing_slash():
        checkPath = check_trailing_slash()
        if checkPath is not None: return checkPath

        # Check if url is clean
        result = cleanUrl()
        if result is not None: return result

        # Check that the city name is not home, paperdrift, station paperdrift
        # if check_path_url(): return "/"
        path = check_path_url()
        if path is not None: return path

        # If all good, return None; nothing to do;
        return None


    def checkTrailingQuestion(self):

        # check for /?/ and /??+ path (2 or more question marks);
        ch_qmark = request.full_path
        if ch_qmark == "/?/" or ch_qmark.find("/??") >= 0 :
            # return False # Not okay; redirect
            self.redirect[0] = True
            self.redirect[1] = request.base_url
        # return True # okay


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


    def doHome(self):
        # from jug.control.homeCtl import HomeCtl

        page_obj = PageCtl()
        page_obj.doHome()
        self.router_result = page_obj.getHtml()


    def doSomePathUrl(self, url):

        result = self.doCheckBadPath(url)
        if result is not None:
            self.redirect[0] = True
            self.redirect[1] = result
            return

        page_obj = PageCtl()
        page_obj.doSomePathUrl(url)
        self.router_result = page_obj.getHtml()


    def doRoute(self, sender=True):
        # Using True/False to denote whether we want to return a result to close out; or whether this is just an intermediary check;

        if self.redirect[0] is True:
            return redirect(self.redirect[1], code=301)

        if sender is True:
            return self.getRouter_result()
        # if here, then will implicitly return None


    def doBeforeRequest(self):
        self.doRequestUrl()
        self.checkTrailingQuestion()



    def parseRoute(self):

        # self.doCommon()
        @self.jug.before_request
        def before_request_route():
            # logger.info("---route_common Yay!")
            self.doBeforeRequest()
            return self.doRoute(False)

        @self.jug.route("/")
        def home():
            # logger.info("---in home")
            self.doHome()
            return self.doRoute()

        @self.jug.route('/<path:url>')
        def somePathUrl(url):
            self.doSomePathUrl(url)
            return self.doRoute()

        # @self.jug.after_request
        # def after_request_route(response_object):
        #     # takes a response object and must return a response object; what is a response object?
        #     logger.info("---after_request")
        #     return response_object


    def start(self):
        self.parseRoute()
        return self.jug



## NOTES -----------------------------

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
