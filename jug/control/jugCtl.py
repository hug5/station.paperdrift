from jug.control.routerCtl import RouterCtl


class JugCtl():

    def __init__(self):
        pass

    def start(self):
        ro = RouterCtl()
        return ro.start()
