from jug.lib.logger import logger
# from flask import render_template
from jug.lib.fLib import F
# from jug.lib.weather_api import Weather_api
# from jug.lib.gLib import G
# import random
from jug.lib.news_scrape import News_Scrape
import random



class AjaxCtl:

    def __init__(self, request_data):

        # logger.info('LocationCtl __init__')
        # self.url = url.rstrip('/').capitalize()

        self.action = request_data['action']
        self.data = request_data
        self.result = {}

    def getResult(self):
        return self.result


    def get_Britannica_Location(self, location):
        news_scrapeO = News_Scrape()
        news_scrapeO.get_britannica(location)
        scrape_result = news_scrapeO.getResult()

        # logger.info(f"--location Brittanica: {location}")

        # if not json_result:

        imageUrl = "https://cdn.britannica.com/37/245037-050-79129D52/world-map-continents-oceans.jpg?w=300&h=1000"
        url = "https://www.britannica.com/Geography-Travel"
        descriptionList = [
            f'{location} is a foresaken settlement in an undisclosed location. Not much is known but that the mayor disappeared with a local barmaid and left his wife and six children in financial destitution. But hope arrived when word appeared that the forlorn wife was sole heir to the Snickers estate. Soon she was flowing in chocolate and romantic suitors as far as her cocoa eyes could see.',
            f'{location} is a favorite tropical haven in the Pacific among the jet-setting cognoscente. The island enjoys daily sun and upscale tourists three months out of the calendar year and oceans of seafood served by the bucket. According to local lore, Poseidon and Amphitrite enjoyed {location} as a summer palace and constructed giant sand chateaus on the beach with fixtures and indoor plumbing that can still be observed today.',
            f'{location} was established as a fortification in 1392 in the steppes of Siberia. Although the fort proved unsuccessful, its inhabitants survived half a dozen seasons on a diet of sheep, turnip and rye. While discipline and comraderie was strong among the young warriors, fighting broke out when a woman arrived and spread gossip and rumors. It would seem that there\'s more than one way to conquer a fort.',
            f'{location} was originally founded as a penal colony in the remote forested hills. Indebted men chopped trees and women of ill repute collected local vegetation. Carpenters produced barrels, tables and chairs. And fruits and vegetables were compressed into fine wine and green libations. Within a number of years exports boomed and profits flowed to the industrious colony freeing felonious men and women from their debts.'
        ]
        # Randomly choose 1
        description = descriptionList[random.randrange(0, len(descriptionList))]

        # In case any values are missing, replace with fiction:
        json_result = {}
        json_result["title"] = scrape_result.get("title", location)  # City
        json_result["url"] = scrape_result.get("url", url)
        json_result["description"] = scrape_result.get("description", description)
        json_result["imageUrl"] = scrape_result.get("imageUrl", imageUrl)

        json_result["status"] = "ok"

        self.result = json_result

    def get_news_db(self):
        # Get news items from MariaDB
        # F.uwsgi_log("Call HomeDb")
        try:
            from jug.dbo.homeDb import HomeDb
            home_obj = HomeDb()
            result_list = home_obj.doHomeDb()
            logger.info(f'reqs: {result_list}')

        except Exception as e:
            logger.info(f'HomeDb exception: {e}')

            result_list = ["Walking After Eating Is a Science-Backed Way To Lose Weight, but Experts Say Timing Is Crucial."]

        logger.info(f'HomeDb result list: {result_list}')

        return result_list


    def get_news_scrape(self):

        try:
            # Get news item from Yahoo News with request
            news_scrapeO = News_Scrape()
            # result_list = news_scrapeO.get_news()[0]
            news_scrapeO.get_news()
            result_list = news_scrapeO.getResult()
            # returning multiarray;
            # first is the headline; 2nd the link;
            # [0]: get back just the headlines
        except Exception as e:
            logger.info(f'News_Scrape exception: {e}')
            result_list = []

        return result_list


    def get_news_result(self):

        result_list = self.get_news_scrape()
        # result_list2 = self.get_news_db

        # logger.info(f'99999999999 -- News_Scrape result list: {result_list}')

        # Combine 2 lists:
        # result_list.extend(result_list2)

        # If no news, then make up fake ones:
        if len(result_list) < 1:
            link = "https://news.yahoo.com/"
            result_list = [
                ["Walking After Eating Is a Science-Backed Way To Lose Weight, but Experts Say Timing Is Crucial.", link],
                ["Citrus fruits are considered a superfood. But can they also help you sleep or avoid motion sickness?", link],
                ["Could fungi actually cause a zombie apocalypse?", link]
            ]

        # randomize list
        random.shuffle(result_list)

        json_result = {}
        json_result["status"] = "ok"
        json_result["news_result"] = result_list

        # logger.info(f'json reqs: {json_result}')

        self.result = json_result

    def get_location(self):
        city = self.data.get("city", False)
        if not city:
            self.result = {
                "status" : "bad",
                "error_message" : "No location."
            }
            return

        self.get_Britannica_Location(F.unhesc(city))
        # escaping the city because when there's a space between words
        # and Britannica can't find it, it results in Las%20Vegas; there's
        # a %20 characters; but if Britcannia finds it, then it seems to
        # remove it; The trouble are the instances when it doesn't find it;



    def doAjax(self):

        if self.action == "get_location":
            self.get_location()
        ###
          # if self.action == "get_location":
          #     city = self.data.get("city", False)
          #     if not city:
          #         self.result = {
          #             "status" : "bad",
          #             "error_message" : "No location."
          #         }
          #         return


          #     self.get_Britannica_Location(F.unhesc(city))
          #     # escaping the city because when there's a space between words
          #     # and Britannica can't find it, it results in Las%20Vegas; there's
          #     # a %20 characters; but if Britcannia finds it, then it seems to
          #     # remove it; The trouble are the instances when it doesn't find it;

        elif self.action == "get_news_result":
            self.get_news_result()


