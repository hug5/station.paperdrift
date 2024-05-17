# from flask import Flask
# from jug import control
# from jug.control import index
# from jug import control
# from jug import control


# def start():

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
# jug = start()

# from control import controller

# # jug = controller.Controller().doRoute()
# c = controller.Controller()

# jug = c.doRoute()

# from jug.html import domHtml

# jug = domHtml.DomHtml.doHtml()


# def doInit():
#     return "init"


#@jug.route("/<arg>")
#def subpath(arg):
#    return "<p>yahoo2 " + arg + "</p>"

#@jug.route('/', defaults={'path1': ''})
# if you also want to catch root; see URL Route Registrations

from flask import Flask


jug = Flask(
    __name__,
    template_folder="html"
)

@jug.route("/")
def home():
    # return "<p>Hello3</p>"
    # from jug.control import domHtml
    # return domHtml.result


    # from html import domHtml
    return "hello"
    # result = domHtml.DomHtml().doHtml("Home")
    # return result


@jug.route('/<path:url>')
def pathUrl(url):
    return "<b>%s</b>" %url

