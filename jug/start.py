
# os.chdir("/home/h5/DATA/zData/Coding/Projects/webdev/station.paperdrift/jug")
# import os
# print(os.getcwd())

# from jug.control.routerCtl import RouterCtl
from jug.control.jugCtl import JugCtl

# ....

# from jug.control import routerCtl
# jug = routerCtl.RouterCtl().start()
  # This works

# ....

# jug = RouterCtl().start()
  # this works

# ....

# This  version should create a new RouterCtl objects;
# But still only 1 instance seems to be created, and shared among users;
# Flask seems to create 1 instance and just reuse it over and over!...
# mug = RouterCtl()
# jug = mug.start()
  # This works
# ....


mug = JugCtl()
jug = mug.start()



