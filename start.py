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

# from jug import init

# # jug = controller.Controller().doRoute()
# jug = init.doInit()


# from jug.html import domHtml

# jug = domHtml.DomHtml.doHtml()





#@jug.route("/<arg>")
#def subpath(arg):
#    return "<p>yahoo2 " + arg + "</p>"

#@jug.route('/', defaults={'path1': ''})
# if you also want to catch root; see URL Route Registrations

# import os cwd = os.getcwd() to pwd within python



from flask import Flask


jug = Flask(
    __name__,
    template_folder="html",
    root_path="/home/h5/DATA/zData/Coding/Projects/webdev/paperdrift"
)

# root_path
# template_folder
# instance_path='/path/to/instance/folder'


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




