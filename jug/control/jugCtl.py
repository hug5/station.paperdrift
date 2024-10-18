from jug.lib.logger import logger

from flask import Flask, redirect, request

# from jug.dbo import dbc
from jug.lib.f import F
from jug.lib.g import G
from pathlib import Path
import tomli
import re
from urllib import parse
from jug.control.pageCtl import PageCtl


class JugCtl():

    def __init__(self):
        logger.info('                          ')
        logger.info('                          ')
        logger.info('XXXXXXXXXXXXXXXXX')
        logger.info('XXXXXXXXXXXXXXXXX')
        logger.info('==== Begin JugCtl Init ===')

        dir_html = "../html"

        self.jug = Flask(
            __name__,
            # template_folder="jug/html"
            template_folder=dir_html,
        )

        # self.jug.debug = True

    def init(self):

        self.article = ''
        self.header = ''
        self.footer = ''
        # self.retry_counter = 0
          # This isn't going to work when the variable is here;
          # On each request, will get reset to 0;

        self.response_obj = False
        self.redirect = [False, '']

        logger.info('---init---')

        logger.info(f'Anything in G BEFORE?: [{G.api}][{G.db}][{G.site}][{G.location}]')
        # G.init()


        self.setConfig_toml()
        logger.info(f'Anything in G AFTER?: [{G.api}][{G.db}][{G.site}][{G.location}]')

        # logger.info(f'Anything in G AFTER?: [{G.api}][{G.db}][{G.site}]')

        # G.get_db()
        # G.get_api()
        # G.get_site()




    def getResponse_obj(self):
        return self.response_obj

    def setConfig_toml(self):

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
            G.site["baseUrl"] = config_toml["site"]["baseUrl"]

        except FileNotFoundError as e:
            logger.exception(f"config.toml Load Error: {e}")
        except Exception as e:
            logger.exception(f"setConfig_toml Error: {e}")
        finally:
            # logger.info(f'weatherAPI_key: {G["weatherAPI_key"]}')
            logger.info(f'weatherAPI_key: {G.api["weatherAPI_key"]}')
            # logger.info(f'Anything in G AFTER?: [{G.api}][{G.db}][{G.site}]')



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
            # logger.info(f'pre url3 in home list: {self.redirect}')

            # If url path is any of these, then go home;
            home_list = ["home", "paperdrift", "station paperdrift", "station"]
            url2 = url.lower()


            # check for home or paperdrift in url; if so, go to root url;
            url3 = url2.rstrip('/')

            # if url3 in home_list:
            #     # logger.info("---redirecting to /")
            #     self.redirect = [True, "/"]

            # tuple ternary operator:
            self.redirect = ([False, ''], [True, '/']) [url3 in home_list]

            # logger.info(f'post url3 in home list: {self.redirect}')




        def check_trailing_slash():
            # Check there is trailing slash in paths;
            # nonlocal checkPath
            # nonlocal url

            # check that url ends in /
            checkPath = F.checkPathSlash(url)
            # if checkPath is not True:
            #     # return checkPath
            #     self.redirect = [True, checkPath]
            #     # return False

            self.redirect = ([False, ""], [True, checkPath])[checkPath is not True]


        def cleanUrl():
            # nonlocal url
            url2 = url.rstrip('/')

            # remove non-alphanumeric characters, but allow for space
            # all bad characters will be replaced with space;
            # then later we'll remove redundant spaces;
            new_url = re.sub(r'[^%a-zA-Z0-9\- ]', ' ', url2)
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
            redirect_url2 = f"/{new_url2}/"
            logger.info("---redirect_url: " + redirect_url2)

            # Don't need to escape since we removed all bad characters;
            # escaped_url = F.hesc(new_url)

            # if new_url2 != url2:
            #     logger.info(f'Cleaned url: {new_url2} : {url2}')
            #     # return "/" + new_url2 + "/"
            #     self.redirect = [True, "/" + new_url2 + "/"]
            #     # return False

            self.redirect = ([False, ''], [True, redirect_url2])[new_url2 != url2]

            # else:
            #     # logger.info(f'good url: {escaped_url}')
            #     logger.info(f'Good url: {new_url2}')
            # return None

            # clean_text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
            # print(clean_text)


        # check_trailing_slash()
        # if self.redirect[0] is True: return None
        # cleanUrl()
        # if self.redirect[0] is True: return None
        # check_path_url()


        # if self.redirect[0] is True: return None


    def checkTrailingQuestion(self):
        pass
        # # check for /?/ and /??+ path (2 or more question marks);
        # # ch_qmark = request.full_path
        # ch_qmark = request.environ["REQUEST_URI"]

        # # if ch_qmark == "/?/" or ch_qmark.find("/??") >= 0 :
        # if ch_qmark == "/?/" or ch_qmark.find("/?") >= 0 :
        #     # return False # Not okay; redirect
        #     logger.info(f"---found ? {request.base_url}")
        #     self.redirect = [True, request.base_url]

    def cleanUrl(self, url):

        url2 = parse.unquote_plus(url)
        url3 = url2.replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('', '').replace('<', '').replace('>', '').replace('?', '').replace('@', '').replace('*', '').replace('~', '').replace('!', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('(', '').replace(')', '').replace(',', '').replace(';', '').replace('+', '').replace('.', '')
        url4 = ' '.join(url3.split())

        url5 = parse.quote_plus(url4, safe="/", encoding="utf-8", errors='replace')

        # Return clean url with slashes
        return f'/{url5}/'

    def checkUrl(self):

        logger.info(f'Beg. state self.redirect: {self.redirect}')

        req_url = request.environ["REQUEST_URI"]
        url_list = req_url.split("/")
        # Home: ['', '']
        # Home: ['', '?asdf']
        # some path: ['', 'san%20diego', '?']
        # url1 = url_list[1]

        # Was trying to catch any suffix beginning with #, but can't seem to do it;
        # There doesn't seem to be a way to grab that value or its existence;
        # parsed_url = parse.urlparse(req_url)
        # fragment = parsed_url[5]
        # logger.info(f'***url_fragment: {parsed_url}')
        ##:: ParseResult(scheme='https', netloc='station.paperdrift.com', path='/first second/third fourth/', params='', query='hello=goodbye&ciao=buenes', fragmenurlurlt='marker')


        url_list_len = len(url_list)
        logger.info(f'***checkUrl: {url_list} : {url_list_len}')

        # We're at home page
        if url_list_len == 2 and url_list[1] != '':
            # r_url = "/"
            r_url = G.site["baseUrl"]
            logger.info(f'***checkUrl, badurl: "{r_url}"')
            self.redirect = [True, r_url]

        # If like this: ['', 'san%20diego', 'asdf', ''], or more;
        # Then too many paths; redirect to index 1
        if url_list_len >= 4:
            url = url_list[1]
            r_url = self.cleanUrl(url)
            logger.info(f'***checkUrl, badurl: "{r_url}"')
            self.redirect = [True, r_url]

        # if like this: ['', 'san%20diego', '?',]
        # Then check index 1 and 2
        if url_list_len == 3:
            if url_list[2] != '':
                url = url_list[1]
                r_url = self.cleanUrl(url)
                logger.info(f'***checkUrl, badurl: "{r_url}"')
                self.redirect = [True, r_url]

            else:
                r_url = self.cleanUrl(url_list[1])
                url = f'/{url_list[1]}/'
                if r_url != url:
                    logger.info(f'***checkUrl, badurl: "{r_url}"')
                    self.redirect = [True, r_url]

        logger.info(f'End. state self.redirect: {self.redirect}')

        # self.redirect = [False, '']


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
        self.response_obj = page_obj.getHtml()


    def doSomePathUrl(self, url):

        # self.doCheckBadPath(url)
        # if self.redirect[0] is True:
        #     return self.redirect[1]

        page_obj = PageCtl()
        page_obj.doSomePathUrl(url)
        self.response_obj = page_obj.getHtml()


    def doRoute(self, sender=True):
        # Using True/False to denote whether we want to return a result to close out; or whether this is just an intermediary check;

        if self.redirect[0] is True:
            # self.retry_counter += 1
            # if self.retry_counter > 1:
            #     self.redirect[1] = G.site["baseUrl"]
            #     logger.info(f'---Borking!--- {self.retry_counter}')
            #     self.retry_counter = 0

            logger.info(f'--redirecting: {self.redirect[1]}')
            return redirect(self.redirect[1], code=301)

        if sender is True:
            return self.getResponse_obj()
        # if here, then will implicitly return None


    def doBeforeRequest(self):
        self.doRequestUrl()
        # self.checkTrailingQuestion()
        self.checkUrl()


    def parseRoute(self):

        @self.jug.before_request
        def before_request_route():

            self.init()

            logger.info('                          ')
            logger.info('                          ')
            logger.info('0000000000000000')
            logger.info('0000000000000000')
            logger.info("---parseRoute")

            # self.redirect = [False, '']
            self.doBeforeRequest()
            # logger.info("---returning None")
            # return None
            # return self.doRoute(False)
            # Odd that if return None, then no effect;

        @self.jug.route("/")
        def home():
            logger.info("---in home")
            self.doHome()
            return self.doRoute()

        @self.jug.route('/<path:url>/')
        def somePathUrl(url):
            logger.info(f"---in path: {url}")
            self.doSomePathUrl(url)
            return self.doRoute()
            # return None

        # @self.jug.route('/<path:url>/<path:url2>/')
        # def somePathUrl2(url, url2):
        #     logger.info("---in path url2")
        #     self.redirect = [True, f"/{url}/"]
        #     return self.doRoute()


        @self.jug.after_request
        def after_request_route(response_object):
            # Reset this!
            # self.redirect = ["False", '']
            logger.info("---after_request")

            # takes a response object and must return a response object; what is a response object?
            return response_object


    def doJug(self):
        # ro = RouterCtl(self.jug)
        # ro.parseRoute()

        self.parseRoute()
        return self.jug
