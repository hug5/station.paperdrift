from jug.lib.logger import logger

from flask import redirect, request

# from jug.dbo import dbc
from jug.lib.f import F
from jug.lib.g import G
from pathlib import Path
import tomli
import re
from urllib import parse
from jug.control.pageCtl import PageCtl


class RouterCtl():

    def __init__(self, jug):
        self.jug = jug
        logger.info('==== Begin RouterCtl __init__ ===')


    def router_init(self):
        logger.info('---router_init---')

        self.article = ''
        self.header = ''
        self.footer = ''
        # self.retry_counter = 0
          # This isn't going to work when the variable is here;
          # On each request, will get reset to 0;

        self.response_obj = False
        self.redirect = [False, '']

        logger.info(f'---In G BEFORE?: [{G.api}][{G.db}][{G.site}]')
        G.reset()
        logger.info(f'---In G AFTER?: [{G.api}][{G.db}][{G.site}]')

        self.setConfig_toml()



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


    def cleanUrl(self, url):

        url2 = parse.unquote_plus(url)
        url3 = (url2.replace('[', '').replace(']', '').replace('{', '')
                .replace('}', '').replace('', '').replace('<', '').replace('>', '')
                .replace('?', '').replace('@', '').replace('*', '').replace('~', '')
                .replace('!', '').replace('#', '').replace('$', '').replace('%', '')
                .replace('^', '').replace('&', '').replace('(', '').replace(')', '')
                .replace(',', '').replace(';', '').replace('+', '').replace('.', ''))
                # Wrap with parenthesis to break up lines;

        url4 = ' '.join(url3.split())

        url5 = parse.quote_plus(url4, safe="/", encoding="utf-8", errors='replace')

        # Return clean url with slashes
        return f'/{url5}/'

    def checkUrl(self):

        logger.info('---checkUrl')
        logger.info(f'---Beginning state self.redirect variable: {self.redirect}')

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


    def doLocationUrl(self, url):

        # self.doCheckBadPath(url)
        # if self.redirect[0] is True:
        #     return self.redirect[1]

        page_obj = PageCtl()
        page_obj.doLocationUrl(url)
        self.response_obj = page_obj.getHtml()


    def doRoute(self, sender=True):
        # Using True/False to denote whether we want to return a result to close out; or whether this is just an intermediary check;

        if self.redirect[0] is True:
            logger.info(f'--redirecting: {self.redirect[1]}')
            return redirect(self.redirect[1], code=301)

        if sender is True:
            return self.getResponse_obj()
        # if here, then will implicitly return None


    def doBeforeRequest(self):
        self.doRequestUrl()
        self.router_init()
        self.checkUrl()


    def parseRoute(self):

        @self.jug.before_request
        def before_request_route():
            logger.info("---parseRoute: before_request---")
            self.doBeforeRequest()

        @self.jug.route("/")
        def home():
            logger.info("---in home")
            self.doHome()
            return self.doRoute()

        @self.jug.route('/<path:url>/')
        def locationUrl(url):
            logger.info(f"---in path: {url}")
            self.doLocationUrl(url)
            return self.doRoute()
            # return None

        # @self.jug.route('/<path:url>/<path:url2>/')
        # def locationUrl2(url, url2):
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

        @self.jug.teardown_request
        def show_teardown(exception):
            logger.info("##################################")
            logger.info("############ teardown ############")
            logger.info("##################################")
            # Not sure what teardown does;


    # def doJug(self):
    #     # ro = RouterCtl(self.jug)
    #     # ro.parseRoute()

    #     self.parseRoute()
    #     return self.jug


