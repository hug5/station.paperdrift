from jug.lib.logger import logger

from flask import redirect, request, jsonify, session
#, make_response

from jug.lib.fLib import F
from jug.lib.gLib import G
# from pathlib import Path
# import tomli
# import re
from urllib import parse
from jug.control.pageCtl import PageCtl


class RouterCtl():

    def __init__(self, jug):
        self.jug = jug
        logger.info('==== Begin RouterCtl __init__ ===')


    def router_init(self):
        logger.info('---router_init---')

        self.response_obj = None
        self.redirect = [False, '']
        logger.info(f'---In G BEFORE?: [{G.api}][{G.db}][{G.site}]')
        G.reset()
        logger.info(f'---In G AFTER?: [{G.api}][{G.db}][{G.site}]')

        self.setConfig_toml()


        # This makes the session last as per PERMANENT_SESSION_LIFETIME
        session.permanent = True

        session["user"] = "Phoebe"  # Some misc user

        if not session.get("location"):
            session["location"] = []



        # session["location"] = ["los angeles", "fresno"]
        # session.pop('username', None)
        # if "user" in session:                         # user in session
        # user = session["user"]
        # session["user"] = user                      # init session

        G.debug = False
        if self.jug.debug:
            logger.info('---RUNNING DEBUG MODE')
            G.debug = True

    def getResponse_obj(self):
        return self.response_obj

    def setConfig_toml(self):

        try:
            # config_toml_path = Path("jug/conf/config.toml")
            # if not Path(config_toml_path).is_file():
            #     raise FileNotFoundError(f"File Not Found: {config_toml_path}.")

            # with config_toml_path.open(mode='rb') as file_toml:
            #     config_toml = tomli.load(file_toml)
            #     # If bad, should give FileNotFoundError


            config_toml = F.load_config_toml()

            G.api["weatherAPI_key"] = config_toml.get("api", {}).get("weatherAPI_key")
            G.api["weatherAPI_url"] = config_toml.get("api", {}).get("weatherAPI_url")

            G.db["un"] = config_toml["db"]["un"]
            G.db["pw"] = config_toml["db"]["pw"]
            G.db["host"] = config_toml["db"]["host"]
            G.db["port"] = config_toml["db"]["port"]
            G.db["database"] = config_toml["db"]["database"]

            G.site["secret_key"] = config_toml["site"]["secret_key"]
            G.site["name"] = config_toml["site"]["name"]
            G.site["tagline"] = config_toml["site"]["tagline"]
            G.site["keywords"] = config_toml["site"]["keywords"]
            G.site["baseUrl"] = config_toml["site"]["baseUrl"]

        except Exception as e:
            logger.exception(f"setConfig_toml Error: {e}")
        finally:
            pass
            # logger.info(f'weatherAPI_key: {G["weatherAPI_key"]}')
            # logger.info(f'weatherAPI_key: {G.api["weatherAPI_key"]}')
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

# /station.paperdrift.com/anchorage
# ---url_list: "['', 'anchorage']"
# /station.paperdrift.com/anchorage/
# ---url_list: "['', 'anchorage', '']"
# /station.paperdrift.com/ or /station.paperdrift.com
# ---url_list: "['', '']"
# /station.paperdrift.com/? or /station.paperdrift.com?
# ---url_list: "['', '?']"

        url_list_len = len(url_list)
        logger.info(f'***checkUrl: {url_list} : {url_list_len}')

        # We're at home page; home  or location without /
        if url_list_len == 2 and url_list[1] != '':
            r_url = (f'/{url_list[1]}/', G.site["baseUrl"])[url_list[1] == "?"]
            # Do one of python's fake ternary operators;
            # This is equivalent to: res = ("false", "true")[n % 2 == 0]
            # If ? or /?, then redirect to baseUrl; or else append slash
            # Above replaces this longer if/else:
              # if url_list[1] == "?":
              #     # redirect to baseUrl
              #     r_url = G.site["baseUrl"]
              # else:
              #     # redirect to path with slash;
              #     r_url = f'/{url_list[1]}/'

            logger.info(f'***checkUrl, badurl1: "{r_url}"')
            self.redirect = [True, r_url]


        # If like this: ['', 'san%20diego', 'asdf', ''], or more;
        # Then too many paths; redirect to index 1
        if url_list_len >= 4:
            url = url_list[1]
            r_url = self.cleanUrl(url)
            logger.info(f'***checkUrl, badurl2: "{r_url}"')
            self.redirect = [True, r_url]

        # if like this: ['', 'san%20diego', '?',]
        # Then check index 1 and 2
        if url_list_len == 3:
            if url_list[2] != '':
                url = url_list[1]
                r_url = self.cleanUrl(url)
                logger.info(f'***checkUrl, badurl3: "{r_url}"')
                self.redirect = [True, r_url]

            else:
                r_url = self.cleanUrl(url_list[1])
                url = f'/{url_list[1]}/'
                if r_url != url:
                    logger.info(f'***checkUrl, badurl4: "{r_url}"')
                    self.redirect = [True, r_url]

        #/favicon.ico


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


    # def doAjax(self, param):
    def doAjaxPost(self):
        from jug.control.ajaxCtl import AjaxCtl
        logger.info("---ajax POST")

        # if param == "POST":
        #     logger.info("---ajax POST")
        # else:
        #     logger.info("---ajax GET")

        ## Use this syntax if url argument sent:
        # arg_value = request.args.get("action")
          # use with url arguments

        ## Use this syntax if form data sent:
        # arg_value = request.form.get("action")  ## Works
          # Use with forms

        ## Use this syntax if url argument or form data sent:
        # arg_value = request.values.get("action")  ## Works
          # A combinatio of form.get and args.get


        ## Use this syntax when json data sent:
        # request_data = request.get_json(force=True)
        # https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.get_json
        request_data = request.get_json()
        # ajax_action = request_data['action']
        # ajax_city = request_data['city']

        # logger.info(f"---ajax value: {ajax_action} {ajax_city}")

        # if not ajax_city or ajax_action != "get_location":
        #     self.response_obj = jsonify(result)
        #     return


        ajax_obj = AjaxCtl(request_data)
        ajax_obj.doAjax()
        result = ajax_obj.getResult()

        # logger.info(f'---response object (1): {result}')

        try:
            self.response_obj = jsonify(result)
        except Exception as e:
            logger.info(f'---jsonify sexception: {e}')

        # logger.info(f'---response object (2): {self.response_obj}')


    def doHome(self):
        # from jug.control.homeCtl import HomeCtl

        page_obj = PageCtl()
        page_obj.doHome()
        self.response_obj = page_obj.getHtml()


    def doLocationUrl(self, url):

        # self.doCheckBadPath(url)
        # if self.redirect[0] is True:
        #     return self.redirect[1]

        # rock = request.cookies.get('rock')
        # logger.info(f'rock: {rock}')

        page_obj = PageCtl()
        page_obj.doLocationUrl(url)
        self.response_obj = page_obj.getHtml()


    def doRoute(self, sender=True):
        # Using True/False to denote whether we want to return a result to close out; or whether this is just an intermediary check;

        logger.info(f'doRoute: {self.redirect}')

        if self.redirect[0] is True:
            logger.info(f'--redirecting: {self.redirect[1]}')
            return redirect(self.redirect[1], code=301)

        if sender is True:
            # resp = make_response(self.response_obj)
            # resp.set_cookie('paper', '1234', samesite='Lax', secure=True)
            # resp.set_cookie('rock', '1234', samesite='Lax', secure=True, max_age=7776000)
            # resp.set_cookie('scissor', '1234')
            logger.info(f'sender is true: {self.redirect}')
            resp = self.response_obj
            return resp



        logger.info(f'sender is NOT True: {self.redirect}')

        # return self.getResponse_obj()
        # if here, then will implicitly return None

        # const jsonData = { name: "John", age: 32 };
        # document.cookie = "userData=" + encodeURIComponent(JSON.stringify(jsonData));
        # const cookies = document.cookie.split('; ');
        # const userDataCookie = cookies.find(row => row.startsWith('userData='));
        # const userData = userDataCookie ? JSON.parse(decodeURIComponent(userDataCookie.split('=')[1])) : null;


    def doBeforeRequest(self):
        logger.info("---doBeforeRequest: Start")

        self.doRequestUrl()
        self.router_init()
        self.checkUrl()
        logger.info("---doBeforeRequest: Finished")


    def parseRoute(self):

        @self.jug.before_request
        def before_request_route():
            logger.info("---parseRoute: before_request---")
            self.doBeforeRequest()

            result = self.doRoute(False)
            if result is not None:
                return result

            # // 2025-02-22 Sat 01:07
            # Appears that the routs will catch urls without slash suffix;
            # But doesn't catch /?, /city/? or /city/xyx

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

        # @self.jug.route('/<path:url>/<path:url2>/')
        # def locationUrl2(url, url2):
        #     logger.info("---in path url2")
        #     self.redirect = [True, f"/{url}/"]
        #     return self.doRoute()


        # @self.jug.route('/ajax/', methods=['GET', 'POST'])
        @self.jug.route('/ajax/', methods=['POST'])
        def ajaxPost():
            logger.info("---in path: ajax")
            # self.doAjax(request.method)
            self.doAjaxPost()
            return self.doRoute()


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



    ######################################
      # def doJug(self):
      #     # ro = RouterCtl(self.jug)
      #     # ro.parseRoute()

      #     self.parseRoute()
      #     return self.jug


