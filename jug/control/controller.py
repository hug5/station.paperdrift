from flask import Flask



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


class Controller:

    def __init__(self):

        self.jug = Flask(
            __name__,
            template_folder="jug/html"
        )


    def doRoute(self):

        @self.jug.route("/")
        def home():
            # return "<p>Hello3</p>"
            # from jug.control import domHtml
            # return domHtml.result

            from ..html import domHtml
            result = domHtml.DomHtml().doHtml("Home")
            return result


        @self.jug.route('/<path:url>')
        def pathUrl(url):
            return "<b>%s</b>" %url

        return self.jug

