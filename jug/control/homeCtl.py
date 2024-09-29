# import logging
# logger = logging.getLogger(__name__)
from jug.lib.logger import logger

from flask import render_template
from jug.lib import gLib
from jug.dbo import homeDb
from jug.control import reqsCtl
# from jug.start import jug
import random

class HomeCtl():

    def __init__(self):
        pass


    def doHome(self):

        pop = gLib.getPop()
        moon_phase = gLib.getMoon()  # returns list

        logger.info('Call HomeDb')
        # gLib.uwsgi_log("Call HomeDb")

        h_obj = homeDb.HomeDb()
        result_list = h_obj.doStart()
        logger.info(f'reqs: {result_list}')

        r_obj = reqsCtl.ReqsCtl()
        result_list2 = r_obj.get_yahoo_news()[0]
        # returning multiarray;
        # first is the headline; 2nd the link;

        news_list = result_list2 + result_list

        random.shuffle(news_list)

        logger.info(f'reqs: {news_list}')

        return render_template(
            "homeHtml.jinja",
            population = pop,
            moon_phase = moon_phase,
            # db_result = db_result,
            news_result = news_list
            # header = headerHtml
            # code=moon
        )


    def doStart(self):
        return self.doHome()

