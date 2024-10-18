from jug.lib.logger import logger

from flask import Flask
from jug.control.routerCtl import RouterCtl

class JugCtl():

    def __init__(self):
        logger.info('                          ')
        logger.info('                          ')
        logger.info('XXXXXXXXXXXXXXXXX')
        logger.info('XXXXXXXXXXXXXXXXX')
        logger.info('==== Begin JugCtl __init__ ===')

        self.jug = Flask(
            __name__,
            template_folder="html",
            # static_folder="www/static",

        )

        # self.jug.debug = True

        logger.info(f'====root_path: {self.jug.root_path}')
        logger.info(f'====instance_path: {self.jug.instance_path}')
        # root_path:     /srv/http/station.paperdrift/jug/control
        # root_path:     /srv/http/station.paperdrift/jug
            # If put the flask instance here, then the root_path
            # is set in /jug, not /jug/control
        # instance_path: /srv/http/station.paperdrift/instance

        # https://flask.palletsprojects.com/en/2.3.x/api/
        # static_url_path
        # static_folder
        # instance_path
        # root_path
        # template_folder


    def doJug(self):
        ro = RouterCtl(self.jug)
        ro.parseRoute()
        # self.parseRoute()
        return self.jug



mug = JugCtl()
jug = mug.doJug()