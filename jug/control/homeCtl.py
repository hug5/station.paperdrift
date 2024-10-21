# import logging
# logger = logging.getLogger(__name__)
from jug.lib.logger import logger

from flask import render_template, session

from jug.lib.fLib import F

from jug.lib import news_scrape
# from jug.start import jug
import random
from jug.lib.weather_api import Weather_api
from jug.lib.gLib import G


class HomeCtl():

    def __init__(self):
        logger.info('HomeCtl __init__')
        self.config = {}
        self.html = ''
        self.locations = {}


    def getHtml(self):
        return self.html

    def getConfig(self):
        return self.config

    def doConfig(self):

        self.config = {
            'site_title' : f"{G.site['name']} | {G.site['tagline']}"
        }

    def getWeather(self):

        location = "Santa Barbara" # for home page, default to Santa Barbara
        weather_obj = Weather_api()
        weatherDict = weather_obj.do_weather(location)
        # logger.info(f'weather: {weatherDict}')
        return weatherDict

    # # Doing ajax now;
    # def get_breaking_news(self):

        # # Get news items from MariaDB
        # # F.uwsgi_log("Call HomeDb")

        # try:
        #     from jug.dbo.homeDb import HomeDb
        #     home_obj = HomeDb()
        #     result_list = home_obj.start()
        #     logger.info(f'reqs: {result_list}')

        # except Exception as e:
        #     result_list = ["Walking After Eating Is a Science-Backed Way To Lose Weight, but Experts Say Timing Is Crucial."]
        #     pass

        # logger.info(f'HomeDb result list: {result_list}')



        # try:
        #     # Get news item from Yahoo News with request
        #     news_scrapeO = news_scrape.News_Scrape()
        #     result_list2 = news_scrapeO.get_yahoo_news()[0]
        # except Exception as e:
        #     result_list2 = ["Citrus fruits are considered a superfood. But can they also help you sleep or avoid motion sickness?"]
        #     pass

        # logger.info(f'News_Scrape result list: {result_list2}')

        # # returning multiarray;
        # # first is the headline; 2nd the link;
        # # [0]: get back just the headlines

        # # Combine 2 lists:
        # result_list.extend(result_list2)
        # # news_list = result_list2 + result_list

        # # Randomize the list
        # random.shuffle(result_list)
        # logger.info(f'reqs: {result_list}')

        # return result_list


    def getMoon(self, moon_phase):
        return F.getMoon(moon_phase)

    def getAdverb(self):
        return F.getAdverb()

    def getLocations(self):

        verb_list = [
            "Barrel",
            "Crawl",
            "Cruise",
            "Dart",
            "Drive",
            "Float",
            "Gallop",
            "Hasten",
            "Hustle",
            "Jog",
            "Lumber",
            "Moonwalk",
            "Sail",
            "Scoot",
            "Scram",
            "Scurry",
            "Skedaddle",
            "Sleepwalk",
            "Sprint",
            "Swim",
        ]

        def get_verb():
            return verb_list[random.randrange(0, len(verb_list))]

        self.locations = {
            "chihuahua" : "Yap to Chihuahua",
            "anchorage" : "Sled to Anchorage",
            "chicago" : "Trading Chicago",
            "phoenix" : "Soar to Phoenix",
            "bangkok" : "Sawadee Bangkok",
            "atlantic+city" : "Roll to Atlantic City",
            "mumbai" : "Flying Mumbai",
            "manila" : "Jungle in Manila",
            "the+hague" : "Charge to The Hague",
            "samarkand" : "Ride to Samarkand",
            "beirut" : "Bunker to Beirut",
            "goleta" : "Surf to Goleta",
            "topeka" : "Twisting Topeka",
            "hanoi" : "Helicopter to Hanoi",
            "cairo" : "Float to Cairo",
            "barcelona" : "Flamingo to Barcelona",
            "casablanca" : "Round Up Casablanca",
            "shanghai" : "Abscond to Shanghai",
        }

        for i in session["location"]:
            if not self.locations.get(i):
                self.locations[i] = f"{get_verb()} to {i.replace('+', ' ').title()}"

        return self.locations


    def doHome(self):

        weatherDict = self.getWeather()
        self.doConfig()

        locations = self.getLocations()

        self.html = render_template(
            "homeHtml.jinja",
            locations = locations,
            population = F.getPop(),
            adv = self.getAdverb(),
            moon_phase = weatherDict["moon_phase"],
            # news_result = self.get_breaking_news(),
            news_result = [],
            weatherDict = weatherDict,
            local_datetime = weatherDict["datetime"],
            country = weatherDict["country"]
        )

