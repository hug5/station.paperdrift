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

    # def get_Britannica_Location(self, location):
        # news_scrapeO = news_scrape.News_Scrape()
        # scrape_result = news_scrapeO.get_britannica(location)

        # # if not json_result:

        # imageUrl = "https://cdn.britannica.com/37/245037-050-79129D52/world-map-continents-oceans.jpg?w=300&h=1000"
        # url = "https://www.britannica.com/Geography-Travel"
        # descriptionList = [
        #     f'{location} is a shadowy settlement in an undisclosed location. Not much is known except that the mayor ran off with the barmaid and left his wife and seven children in penury destitution. But all was not lost as word arrived she was sole heir to the Snickers estate. Soon she was flowing in chocolate and romantic suitors as far as the cocoa eye can see.',
        #     f'{location} is a tropical haven in the Pacific. It enjoys year round sun, upscale tourists three months out of the calendar year, and tons of seafood sold by the bucket. According to local lore, Poseidon and Amphitrite used {location} as a summer palace and made giant sand chateaus on the beach with fixtures and indoor plumbing that can still be seen today.',
        #     f'{location} was established as a fortification in 1392 in the steppes of Siberia. Although the fort proved unsuccessful, its inhabitants survived half a dozen seasons on a diet of sheep, turnip and rye. While discipline and comraderie was strong among the young warriors, fighting broke out when a woman arrived and began to spread gossip and rumors. It would seem that there\'s more than one way to conquer a fort.',
        #     f'{location} was originally founded as a debtor penal colony in forested hills in the high mountains. Men were put to work chopping trees and women labored long hours collecting local vegetation. Carpenters produced barrels, tables and chairs. And women compressed fruits and vegetables into wine and green libations. Soon exports boomed and profits flowed to the industrial colony, freeing all men and women from their debts.'
        # ]
        # # Randomly choose 1
        # description = descriptionList[random.randrange(0, len(descriptionList))]

        # # In case any values are missing, replace with fiction:
        # json_result = {}
        # json_result["title"] = scrape_result.get("title", location)  # City
        # json_result["url"] = scrape_result.get("url", url)
        # json_result["description"] = scrape_result.get("description", description)
        # json_result["imageUrl"] = scrape_result.get("imageUrl", imageUrl)

        # return json_result

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
        weatherDict = weather_obj.do_weather(location)
        logger.info(f'weather: {weatherDict}')
        return weatherDict


    def doLocation(self):

        weatherDict = self.getWeather()
        # Let's always use canoncial name from weatherAPI, not name entered by user,
        # unless weatherapi couldn't find it; then the bad name is used;
        # location = weatherDict.get("location")
          # This would be the safe way to do it... but so much trouble!!
          # how mnay times do I have to error check?!

        location = weatherDict.get("location")
        location_info = {}
        # location_info = self.get_Britannica_Location(location)
        self.doConfig(location)

        location_set = set(session["location"])
        location_set.add(location.lower().replace(" ", "+"))

        session["location"] = list(location_set)


        logger.info(f'@@@@@ session location: {session["location"]}')



        # logger.info(f'session location: {session["location"]}')


        self.html = render_template(
            "locationHtml.jinja",
            city = location,
            location_info = location_info,
            population = self.getPop(),
            moon_phase = weatherDict["moon_phase"],
            adv = self.getAdverb(),
            adj = self.getAdjective(),
            famousSyn = self.getFamousSyn(),
            famousFor = self.getFamousFor(),
            pronoun = self.getPronoun(),
            weatherDict = weatherDict,
            local_datetime = weatherDict["datetime"],
            country = weatherDict["country"]
        )


