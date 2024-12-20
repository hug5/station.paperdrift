# import logging
# logger = logging.getLogger(__name__)
from jug.lib.logger import logger

from flask import render_template, session

from jug.lib.fLib import F
from jug.lib.gLib import G

# from jug.lib import news_scrape
# from jug.start import jug
import random
from jug.lib.weather_api import Weather_api


class HomeCtl():

    def __init__(self):
        logger.info('---HomeCtl __init__')
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

        logger.info('---getWeather: BEFORE')

        location = "Santa Barbara" # for home page, default to Santa Barbara
        weather_obj = Weather_api()
        weather_obj.do_weather(location)
        weatherDict = weather_obj.getResult()
        # logger.info(f'weather: {weatherDict}')

        logger.info('---getWeather: AFTER')

        return weatherDict


    def getMoon(self, moon_phase):
        return F.getMoon(moon_phase)

    def getAdverb(self):
        return F.getAdverb()

    def getLocations(self):


        def get_verb():
            return F.getVerb()

        self.locations = {
            "chihuahua" : "Yap to Chihuahua",
            "anchorage" : "Sled to Anchorage",
            "chicago" : "Trade to Chicago",
            "phoenix" : "Soar to Phoenix",
            "bangkok" : "Sawadee to Bangkok",
            "atlantic+city" : "Roll to Atlantic City",
            "mumbai" : "Fly to Mumbai",
            "manila" : "Swing to Manila",
            "the+hague" : "Charge to The Hague",
            "samarkand" : "Ride to Samarkand",
            "beirut" : "Bunker to Beirut",
            "malibu" : "Surf to Malibu",
            "topeka" : "Twist to Topeka",
            "hanoi" : "Airdrop to Hanoi",
            "cairo" : "Float to Cairo",
            "barcelona" : "Flamingo to Barcelona",
            "casablanca" : "Round Up to Casablanca",
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
            moon_phase = weatherDict.get("moon_phase"),
            # news_result = self.get_breaking_news(),
            news_result = [],
            weatherDict = weatherDict,
            local_datetime = weatherDict.get("datetime"),
            country = weatherDict.get("country")
        )

