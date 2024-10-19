from jug.lib.logger import logger

from flask import Flask
from jug.control.routerCtl import RouterCtl

class JugCtl():

    def __init__(self):
        logger.info('                          ')
        logger.info('XXXXXXXXXXXXXXXXX')
        logger.info('                          ')
        logger.info('==== Begin JugCtl __init__ ===')
        logger.info('                          ')
        logger.info('XXXXXXXXXXXXXXXXX')
        logger.info('                          ')

        self.jug = Flask(
            __name__,

            template_folder="html",

            # custom static; static is default
            # This lets flask serve static files using flask server
            static_folder="www/static",

        )

        # https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
        # $ python -c 'import secrets; print(secrets.token_hex())'
        # cd97c91dae2d43a9b8fa3d3d6d5930bf1b1a5c59553a292b2b2c4edbf099fc3f

        # https://flask.palletsprojects.com/en/3.0.x/web-security/#security-cookie
        self.jug.config.update(
            # TESTING=True,
            SECRET_KEY='cd97c91dae2d43a9b8fa3d3d6d5930bf1b1a5c59553a292b2b2c4edbf099fc3f',
            SESSION_COOKIE_SECURE = True,
            SESSION_COOKIE_SAMESITE = 'Lax'  # Strict, None
        )

        # As an environment variable:
        # FLASK_DEBUG=1

        # session["name"] = "Bob"

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

# ---------------------------------------------------

mug = JugCtl()
jug = mug.doJug()