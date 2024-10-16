# import logging
# logger = logging.getLogger(__name__)
from jug.lib.logger import logger

from flask import render_template
from jug.lib.f import F
from jug.dbo import homeDb
from jug.lib import news_scrape
# from jug.start import jug
import random
from jug.lib.weather_api import Weather_api
from jug.lib.g import G


class HomeCtl():

    def __init__(self):
        logger.info('HomeCtl __init__')

        self.config = {}
        self.html = ''

        pass

    def getHtml(self):
        return self.html

    def getConfig(self):
        return self.config

    def doConfig(self):

        self.config = {
            'site_title' : f"{G.site['name']} | {G.site['tagline']}"
        }

    def getWeather(self):
        location = "Santa Barbara"
        weather_obj = Weather_api()
        weatherDict = weather_obj.do_weather(location)
        # logger.info(f'weather: {weatherDict}')
        return weatherDict

    def get_breaking_news(self):


        # Get news items from MariaDB
        # F.uwsgi_log("Call HomeDb")

        # logger.info('Call HomeDb')
        homeO = homeDb.HomeDb()
        result_list = homeO.start()
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
    def getMoon(self, moon_phase):
        return F.getMoon(moon_phase)

    def getAdverb(self):
        return F.getAdverb()

    def doHome(self):

        weatherDict = self.getWeather()

        self.doConfig()

        # return render_template(
        self.html = render_template(
            "homeHtml.jinja",
            population = F.getPop(),
            adv = self.getAdverb(),
            moon_phase = weatherDict["moon_phase"],
            news_result = self.get_breaking_news(),
            weatherDict = weatherDict,
            local_datetime = weatherDict["datetime"],
            country = weatherDict["country"]
        )


    def start(self):
        # return self.doHome()
        self.doHome()

