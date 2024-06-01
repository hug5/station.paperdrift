
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

# from flask import Flask, render_template
from flask import Flask, redirect
# from ..control import home
# from ..control import gg
# import gf

class ControllerCtl:

    def __init__(self):

        self.jug = Flask(
            __name__,
            template_folder="../html"
        )

        self.article = ''
        self.header = ''
        self.footer = ''

    def doHome(self):

        pass

    def doPath(self):
        pass


    def doRoute(self):

        @self.jug.route("/")
        def home():

            # from html import domHtml
            # from ..html import domHtml
            # result = domHtml.DomHtml().doHtml("Home")
            # return result

            # from ..html import domHtml
            # result = domHtml.DomHtml().doHtml("Home")
            # return render_template(result)
            #   # Doesn't work

            # return (gf.hesc("<p>hello xss</p>"))  # escape the string;
            # return ("<b>hello xss</b>")  # not escaped;

            # return render_template("home.j2") # Calling jinja directly

            # from ..control.home import HomeController
            # c = HomeController()

            from ..control import homeCtl
            obj = homeCtl.HomeCtl()
            return obj.doStart()


        @self.jug.route('/<path:url>')
        def pathUrl(url):
            # return "<b>%s</b>" %url
            # return render_template(
            #     "path.j2",
            #     path=url
            # )
            url2 = url.rstrip('/')
            if url2 != url:
                # 301 /url2
                return redirect('/' + url2)

            from ..control import pathCtl
            obj = pathCtl.PathCtl(url)
            return obj.doStart()

    def doStart(self):
        self.doRoute()
        return self.jug
