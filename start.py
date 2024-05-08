from flask import Flask

def start():

  flap = Flask(__name__)

  @flap.route("/")
  def index():
      return "<p>Hello3</p>"

  #@flap.route("/<arg>")
  #def subpath(arg):
  #    return "<p>yahoo2 " + arg + "</p>"

  #@flap.route('/', defaults={'path1': ''})
  # if you also want to catch root; see URL Route Registrations

  @flap.route('/<path:path1>')
  def catch_all(path1):
      return "The path is : %s" %path1


  return flap


flap = start()
