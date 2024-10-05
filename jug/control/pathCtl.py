from jug.lib.logger import logger
from flask import render_template
from jug.lib import gLib
from jug.lib import weather_api
from jug.control.g import G
import random


class PathCtl:

    def __init__(self, url):
        # self.url = url.rstrip('/').capitalize()
        self.url = url.rstrip('/').title()

        self.config = {}

    def getConfig(self):
        return self.config

    def doConfig(self, title):

        ##
            # $siteName = F::json("config", "siteName");
            # $tagline = F::json("config", "siteTagline");

            # // $title = $arg ? "$b_title | $siteName | $tagline" : "$b_title | $siteName";
            # $title = "$b_title | $siteName";

            # $description = "$b_title, " . F::json("config", "siteDescription");
            # // $keywords    = $b_title . $tags . F::json("config", "siteKeywords");


            # $this->config = [
            #     //"showBillboard"  => false,
            #     //"showSidebar"    => false,
            #     "title"          => $title,
            #     "description"    => $description
            #     // "keywords"       => $keywords
            # ];

        self.config = {
            'site_title' : f"{title} | {G.site['name']}"
        }


    def getPop(self):
        return gLib.getPop()

    def getMoon(self, moon_phase):
        return gLib.getMoon(moon_phase)

    def getAdverb(self):
        return gLib.getAdverb()

    def getAdjective(self):
        return gLib.getAdjective()

    def getPronoun(self):
        return gLib.getPronoun()

    def getFamousFor(self):
        return gLib.getFamousFor()
    def getFamousSyn(self):
        return gLib.getFamousSyn()

    def getWeather(self):

        location = self.url
        weather = weather_api.Weather_api()
        weatherDict = weather.do_weather(location)
        logger.info(f'weather: {weatherDict}')

        return weatherDict


    def doPath(self):

        weatherDict = self.getWeather()

        # Let's always use canoncial name from weatherAPI, not name entered by user,
        # unless weatherapi couldn't find it; then the bad name is used;
        location = weatherDict.get("location")
          # This would be the safe way to do it... but so much trouble!!
          # how mnay times do I have to error check?!

        self.doConfig(location)


        country = weatherDict["country"]
        local_datetime = weatherDict["datetime"]

        moon_phase = self.getMoon(weatherDict["moon_phase"])

        # moon_phase = weatherDict["moon_phase"]
        # t = type(moon_phase)
        # logger.info(f'moonphase: {t}')
        # logger.info(f'moonphase: {moon_phase[0][0]}')
        # logger.info(f'moonphase: {moon_phase[0][1]}')

        return render_template(
            "pathHtml.jinja",
            # city = self.url,
            city = location,
            population = self.getPop(),
            moon_phase = moon_phase,
            adv = self.getAdverb(),
            adj = self.getAdjective(),
            famousSyn = self.getFamousSyn(),
            famousFor = self.getFamousFor(),
            pronoun = self.getPronoun(),
            weatherDict = weatherDict,
            local_datetime = local_datetime,
            country = country
        )


    def doStart(self):
        return self.doPath()

