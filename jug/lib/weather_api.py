from jug.lib.logger import logger

import requests
import json
import random
# import tomli
from jug.lib.gLib import G
from jug.lib.fLib import F




class Weather_api:

    def __init__(self):

        # Base url:
        w_burl = G.api["weatherAPI_url"]

        # weatherAPI key; get key from key module;
        # w_key = "&key=" + weatherAPI_key.wkey
        # w_key = f"&key={G['weatherAPI_key']}"
        w_key = f"&key={G.api['weatherAPI_key']}"

        # weather url, minus location:
        self.w_url = w_burl + w_key + "&q="

        self.result = {}

    def getResult(self):
        return self.result

    def send_req(self, url):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=7)
            logger.info(f'---response status code: {response.status_code}')
            response.encoding = "utf-8"
            return response
        except Exception as e:
            logger.debug(f'!!! send_req error: {e}')
            # convert dictionary to json string;
            return json.dumps({})


    def get_random_location(self):

        country_list = [
            "Moscow",
            "Tehran",
            "Baghdad",
            "Damascus",
            "Beijing",
            "Brasilia",
            "Tokyo",
            "Seoul",
            "Ulaanbaatar",
            "Athens",
            "Paris",
            "London",
            "Munich",
            "Milan",
            "Kinshasa",
            "Lagos",
            "Cairo",
            "Nairobi"
        ]

        # Get random number between 0 and list length - 1
        index = random.randrange(0, len(country_list))
        return country_list[index]

    def make_fake_weather(self, location):

        # We'll end up here if the weatherAPI isn't working
        # Should almost never get here;

        # Return a dictionary with some values that we use;
        return {
            "location": {
                "name": location,
                "country": "Atlantis",
                "localtime": F.getDateTime("basic")
            },
            "current": {
                "temp_c": 25.6,
                "temp_f": 78.1,
                "condition": {
                    "text": "Partly cloudy",
                    "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
                    "code": 1003
                },
                "humidity": 58,
                "cloud": 50,
                "feelslike_c": 27.7,
                "feelslike_f": 81.8,
            },
            "forecast": {
                "forecastday": [
                    {
                        "day": {
                            "maxtemp_c": 22.6,
                            "maxtemp_f": 72.7,
                            "mintemp_c": 18.5,
                            "mintemp_f": 65.3,
                            "avgtemp_c": 20.3,
                            "avgtemp_f": 68.5,
                        },
                        "astro": {
                            "sunrise": "06:47 AM",
                            "sunset": "06:33 PM",
                            "moonrise": "04:36 AM",
                            "moonset": "05:51 PM",
                            "moon_phase": "Waning Crescent",
                            "moon_illumination": 7,
                            "is_moon_up": 0,
                            "is_sun_up": 0
                        }

                    }
                ]
            }
        }

    def call_weather(self, location):

        # location="Los Angeles"
        url = self.w_url + location

        # response = send_req(url)
        # print(response.text)

        result = self.send_req(url)
        # if result is not False:
        # jsonr = json.loads(self.send_req(url).text)

        try:
            # json.loads: parse a JSON string and convert it into a Python Dictionary.
            return json.loads(result.text)
        except Exception as e:
            logger.debug(f'!!! json.loads error: {e}')
            # if error, return empty dictionary
            return {}



    def getMoon_emoji(self, moon_phase=False):
        # moonArr = ['◐', '◑', '◒', '◓', '◔', '◕']
        # return moonArr[random.randrange(0, 6)]
        # return random.choice(moonArr)
          # Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.

        # random.randInt(0, 5)  # This returns from 0 to 5, including 5
        # random.randrange(0,6) # This returns from 0 to 5, excludes 6

        moonList_emoji = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']
        moonList_str = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
        # I forget whwere I got these names? May not necessarily correspond with names from api; Oroginally had New Moon and Full Moon as 'New' and 'Full' but 'Full' was incorrect;

        logger.info(moon_phase)

        # Return the emoji and text
        # If no specific moon phase provided, then get random:
        if  moon_phase:
            for index, moon in enumerate(moonList_str):
                if moon_phase.lower() == moon.lower():
                    return [moonList_str[index], moonList_emoji[index]]
                    # moon_result = [moonList_str[index], moonList_emoji[index]]
                    # logger.info(moon_result)
                    # return moon_result

        logger.info(f"---Bad Moon: No moon match for: {moon_phase}")
        # If still here, then get random moon phase
        max = len(moonList_emoji)
        rnd = random.randrange(0, max)

        return [moonList_str[rnd], moonList_emoji[rnd]]

        # moonDict = {
        #     "New Moon": '🌑',
        #     "Waxing Crescent Moon":'🌒',
        #     "First Quarter Moon":'🌓',
        #     "Waxing Gibbous Moon":'🌔',
        #     "Full Moon":'🌕',
        #     "Waning Gibbous Moon":'🌖',
        #     "Last Quarter Moon":'🌗'
        #     "Waning Crescent Moon":'🌘'
        # }
        # # randomly pop item from dictionary as a list;
        # # Should return as: ["New Moon", "🌑"]

        # moonList = moonDict.popitem()
        # return moonList



    def parse_weather_json(self, jsonr):

        # parse the json
        # Remember that the location may be fake; ie, not match with request;

        try:

            weather = {}

            # Parse json:
            # city = jsonr.get("location['name']", "error")
            # weather["location"] = jsonr.get("location")["name"]
            weather["location"] = jsonr.get("location", {}).get("name")
              # Can also call get multiple times to safely get value;
              # yet if the return is None, then the 2nd call is not safe!

            weather["country"] = jsonr.get("location", {})['country']
            # if weather["country"] == "United States of America" or weather["country"] == "USA United States of America":
            #     weather["country"] = "United States"
            if weather["country"].find("United States") > -1:
                weather["country"] = "United States"

            weather["datetime"] = jsonr.get("location", {})['localtime']

            weather["temp_c"] = jsonr.get("current", {})['temp_c']
            weather["temp_f"] = jsonr.get("current", {})['temp_f']
            weather["feelslike_c"] = jsonr.get("current", {})['feelslike_c']
            weather["feelslike_f"] = jsonr.get("current", {})['feelslike_f']
            weather["humidity"] = jsonr.get("current", {})['humidity']

            weather["condition_text"] = jsonr.get("current", {})['condition']['text']
            weather["condition_icon"] = "https:" + jsonr.get("current", {})['condition']['icon']

            weather["max_temp_c"] = jsonr.get("forecast", {})['forecastday'][0]['day']['maxtemp_c']
            weather["min_temp_c"] = jsonr.get("forecast", {})['forecastday'][0]['day']['mintemp_c']
            weather["max_temp_f"] = jsonr.get("forecast", {})['forecastday'][0]['day']['maxtemp_f']
            weather["min_temp_f"] = jsonr.get("forecast", {})['forecastday'][0]['day']['mintemp_f']
            weather["sunrise"] = jsonr.get("forecast", {})['forecastday'][0]['astro']['sunrise']
            weather["sunset"] = jsonr.get("forecast", {})['forecastday'][0]['astro']['sunset']
            # weather["moon_phase"] = jsonr.get("forecast", {})['forecastday'][0]['astro']['moon_phase']
            moon_phase = jsonr.get("forecast", {})['forecastday'][0]['astro']['moon_phase']

            weather["moon_phase"] = self.getMoon_emoji(moon_phase)
                # will return list:
                # [0] moon name, [1] moon emoji


            # print(weather)
            return weather

        except Exception as e:
            logger.exception("Error parsing weather json")
            return {}
        finally:
            pass


    def do_weather(self, location):

        # if G.debug is True:
        #     return {}

        jsonr = self.call_weather(location)


        # logger.info(f"---json dumps: {json.dumps(jsonr)}")

        # If bad location, then get will default to None
        # result = jsonr.get("location", "other_default_value")
        result = jsonr.get("location")

        # result = None  # Test what happens if None;

        # Let's put a cap on the number of retries in case weatherAPI is down or we can't get access; if down, we'll make up a fake weather dictionary;
        try_counter = 0
        while result is None:
            logger.info('---Weather None; try random location.')

            # If bad location, then try random location:
            jsonr = self.call_weather(self.get_random_location())
            result = jsonr.get("location")

            if result:
                # logger.info('Weather found result')
                # logger.info(json.dumps(jsonr))
                # If a random location is good, then we want to put back the user's
                # Make appear like the original location; not random location;
                jsonr["location"]["name"] = location
                break

            try_counter += 1
            if try_counter > 1:
                # If random location fails, then just make up a completely fake one;
                logger.info('---FFFFFFFFFF WeatherAPI: Get Fake')
                jsonr = self.make_fake_weather(location)
                break


        # return self.parse_weather_json(jsonr)
        self.result = self.parse_weather_json(jsonr)

