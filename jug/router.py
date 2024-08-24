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

        # self.doStart()
        # return self.jug

    def doCommon(self):
        self.header = "header"
        self.footer = "footer"

    def doHome(self):

        # self.doCommon()

        from jug.control import homeCtl
        # import jug.control.homeCtl

        obj = homeCtl.HomeCtl()
        # article_raw = obj.doStart()
        self.article = obj.doStart()

        # article_raw = article_raw.replace('\n', '')
        # self.article = article_raw.replace('    ', '')
        # self.article = article_raw

        pageHtml = render_template(
            "combineHtml.jinja",
            header = self.header,
            footer = self.footer,
            article = self.article
        )

        pageHtml = pageHtml.replace('\n', '')
        return pageHtml.replace('    ', '')


    def doPath(self):
        pass


    def doRoute(self):

        @self.jug.route("/")
        def home():

            # from html import domHtml
            # from html import domHtml
            # result = domHtml.DomHtml().doHtml("Home")
            # return result

            # from html import domHtml
            # result = domHtml.DomHtml().doHtml("Home")
            # return render_template(result)
            #   # Doesn't work

            # return (gf.hesc("<p>hello xss</p>"))  # escape the string;
            # return ("<b>hello xss</b>")  # not escaped;

            # return render_template("home.jinja") # Calling jinja directly

            # from control.home import HomeController
            # c = HomeController()

            return self.doHome()



        @self.jug.route('/<path:url>')
        def pathUrl(url):
            # return "<b>%s</b>" %url
            # return render_template(
            #     "path.jinja",
            #     path=url
            # )
            # url2 = url.rstrip('/')  # right-strip;
                # This always makes sure there's no final slash;
            url2 = url.rstrip('/') + "/"
                # This makes usre there is always a final slash;
            if url2 != url:
                # return "here"
                # 301 /url2   # Not sure what this is about; doesn't seem to work;
                return redirect('/' + url2)
                    # The / makes the redirect at the root; otherwise, will just append the url;
                # if there's a / at url, then redirect to non-slash url;
            # return "there"
            # from control import pathCtl
            # import control.pathCtl
            from jug.control import pathCtl
            obj = pathCtl.PathCtl(url)
            return obj.doStart()

    def doStart(self):
        self.doRoute()
        return self.jug



# from jug import router
# obj = Router()
# jug = obj.doStart()

# jug = Router()

jug = Router().doStart()
