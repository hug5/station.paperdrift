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

from  jug.control import controller

# jug = controller.Controller().doRoute()
c = controller.Controller()

# jug = c.doRoute()
jug = c.doStart()

# from jug.html import domHtml

# jug = domHtml.DomHtml.doHtml()





#@jug.route("/<arg>")
#def subpath(arg):
#    return "<p>yahoo2 " + arg + "</p>"

#@jug.route('/', defaults={'path1': ''})
# if you also want to catch root; see URL Route Registrations