from jug.lib.logger import logger
from flask import session
from flask import render_template
from jug.lib.fLib import F
from jug.lib.weather_api import Weather_api
from jug.lib.gLib import G
# import random
# from jug.lib import news_scrape



class LocationCtl:

    def __init__(self, url):

        logger.info('LocationCtl __init__')
        # self.url = url.rstrip('/').capitalize()
        self.url = url.rstrip('/').title()
        self.config = {}
        self.html = ''


    def getHtml(self):
        return self.html

    def getConfig(self):
        return self.config

    def doConfig(self, title):

        self.config = {
            'site_title' : f"{title} | {G.site['name']}"
        }

    def getPop(self):
        return F.getPop()

    def getMoon(self, moon_phase):
        return F.getMoon(moon_phase)

    def getAdverb(self):
        return F.getAdverb()

    def getAdjective(self):
        return F.getAdjective()

    def getPronoun(self):
        return F.getPronoun()

    def getFamousFor(self):
        return F.getFamousFor()

    def getFamousSyn(self):
        return F.getFamousSyn()

    def getWeather(self):
        location = self.url
        weather_obj = Weather_api()
        weather_obj.do_weather(location)
        weatherDict = weather_obj.getResult()

        logger.info(f'---weather: {weatherDict}')
        return weatherDict


    def doLocation(self):

        weatherDict = self.getWeather()
        # Let's always use canoncial name from weatherAPI, not name entered by user,
        # unless weatherapi couldn't find it; then the bad name is used;

        # This will error if weatherDict is not a dictionary
        # Should always return a dictionary;
        location = weatherDict.get("location", "")
        logger.info(f'@@@@@ weatherDict location: {location}')

        location_info = {}
        # location_info = self.get_Britannica_Location(location)
        self.doConfig(location)

        location_set = set(session["location"])
        location_set.add(location.lower().replace(" ", "+"))

        session["location"] = list(location_set)

        # logger.info(f'@@@@@ session location: {session["location"]}')


        # logger.info(f'session location: {session["location"]}')


        self.html = render_template(
            "locationHtml.jinja",
            city = location,
            location_info = location_info,
            population = self.getPop(),
            moon_phase = weatherDict.get("moon_phase"),
            adv = self.getAdverb(),
            adj = self.getAdjective(),
            famousSyn = self.getFamousSyn(),
            famousFor = self.getFamousFor(),
            pronoun = self.getPronoun(),
            weatherDict = weatherDict,
            local_datetime = weatherDict.get("datetime"),
            country = weatherDict.get("country")
              # Getting country in upper box from weatherAPI;
              # But the country in the description box below comes from Britannia;
              # Could be different!
        )


