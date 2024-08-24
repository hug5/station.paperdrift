###
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
  # from jug.control import controller
  # jug = controller.Controller().doRoute()
  # jug = c.doRoute()

  # from jug.html import domHtml
  # jug = domHtml.DomHtml.doHtml()

  #@jug.route("/<arg>")
  #def subpath(arg):
  #    return "<p>yahoo2 " + arg + "</p>"

  #@jug.route('/', defaults={'path1': ''})
  # if you also want to catch root; see URL Route Registrations

  # -------------------------------------

  # import sys
  # sys.path.append("jug/html")
  # sys.path.append("jug/control")
  # import controller
  # c = controller.Controller()
    # This works

#---------------------------------------------------


# from jug.control.controller import Controller
# c = Controller()

#1
# from jug.control import mainCtl
# obj = mainCtl.MainCtl()
  # This works

#2
from jug import router
obj = router.Router()



# from jug.control import controller
# c = controller.Controller()
  # This works


jug = obj.doStart()
# jug = c.doRoute()


# Examples of starting flask:
  # --app src/hello
  #
  #     Sets the current working directory to src then imports hello.
  # --app hello.web
  #
  #     Imports the path hello.web.
  # --app hello:app2
  #
  #     Uses the app2 Flask instance in hello.
  # --app 'hello:create_app("dev")'
  #
  #     The create_app factory in hello is called with the string 'dev' as the argument.
  #