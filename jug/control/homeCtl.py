# import logging
# logger = logging.getLogger(__name__)
from jug.lib.logger import logger

from flask import render_template
from jug.lib import gLib
from jug.dbo import homeDb
# from jug.start import jug


class HomeCtl():

    def __init__(self):
        pass


    def doHome(self):

        pop = gLib.getPop()
        moon_phase = gLib.getMoon()  # returns list

        logger.info('Call HomeDb')
        # gLib.uwsgi_log("Call HomeDb")

        obj = homeDb.HomeDb()
        db_result = obj.doStart()


        return render_template(
            "homeHtml.jinja",
            population = pop,
            moon_phase = moon_phase,
            db_result = db_result
            # header = headerHtml
            # code=moon
        )


    def doStart(self):
        return self.doHome()

