# import logging
# logger = logging.getLogger(__name__)
from jug.lib.logger import logger

from flask import render_template
from jug.lib import gLib
from jug.dbo import homeDb
from jug.lib import news_scrape
# from jug.start import jug
import random
from jug.lib import weather_api


class HomeCtl():

    def __init__(self):
        pass


    def getWeather(self):

        location = "Santa Barbara"
        weather = weather_api.Weather_api()
        weatherDict = weather.do_weather(location)
        logger.info(f'weather: {weatherDict}')

        return weatherDict

    def get_breaking_news(self):


        # Get news items from MariaDB
        # gLib.uwsgi_log("Call HomeDb")

        # logger.info('Call HomeDb')
        homeO = homeDb.HomeDb()
        result_list = homeO.doStart()
        logger.info(f'reqs: {result_list}')


        # Get news item from Yahoo News with request
        news_scrapeO = news_scrape.News_Scrape()
        result_list2 = news_scrapeO.get_yahoo_news()[0]
        # returning multiarray;
        # first is the headline; 2nd the link;
        # [0]: get back just the headlines

        # Combine 2 lists:
        result_list.extend(result_list2)
        # news_list = result_list2 + result_list

        # Randomize the list
        random.shuffle(result_list)
        logger.info(f'reqs: {result_list}')

        return result_list


    def doHome(self):

        return render_template(
            "homeHtml.jinja",
            population = gLib.getPop(),
            moon_phase = gLib.getMoon(),
            news_result = self.get_breaking_news(),
            weatherDict = self.getWeather()
        )


    def doStart(self):
        return self.doHome()

