import requests
import json
import random
import tomli
from jug.control.g import G



class Weather_api:

    def __init__(self):

        # Base url:
        w_burl = "https://api.weatherapi.com/v1/forecast.json?aqi=no&alerts=no&days=1"

        # weatherAPI key; get key from key module;
        # w_key = "&key=" + weatherAPI_key.wkey
        w_key = f"&key={G['weatherAPI_key']}"

        # weather url, minus location:
        self.w_url = w_burl + w_key + "&q="

        # url = w_url + location


        # with open(config_path, 'rb') as ftoml:
        #     config = tomli.load(ftoml)
        #   # If bad, should give FileNotFoundError

        # self.filename = config['history_source_file']
        # if self.filename == '': raise NameError("No history_source_file")


    def send_req(self, url):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

        # Cookies and sessions?
        # response = requests.Session()

        response = requests.get(url, headers=headers, timeout=7)
        response.encoding = "utf-8"
        return response

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
            "lagos",
            "Cairo",
            "Nairobi"
        ]

        # Get random number between 0 and list length - 1
        index = random.randrange(0, len(country_list))
        return country_list[index]

    def make_fake_weather(self):

        # We'll end up here if the weatherAPI isn't working

        # Return a dictionary with some values that we use;
        return {
            "location": {
                "name": "City of Atlantis",
                "country": "Atlantis",
                "localtime": "15:42"
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
        jsonr = json.loads(self.send_req(url).text)

        return jsonr


    def do_weather(self, location):

        jsonr = self.call_weather(location)

        # If bad location, then get will default to None
        # result = jsonr.get("location", "other_default_value")
        result = jsonr.get("location")

        # Let's put a cap on the number of retries in case weatherAPI is down or we can't get access; if down, we'll make up a fake weather dictionary;
        try_counter = 0
        while result is None:
            # If bad location, then try random location:
            jsonr = self.call_weather(self.get_random_location())
            result = jsonr.get("location")
            try_counter += 1
            if try_counter > 5:
                result = self.make_fake_weather()


        # parse the json
        # Remember that the location may be fake; ie, not match with request;
        try:

            weather = {}

            # Parse json:
            # city = jsonr.get("location['name']", "error")
            weather["location"] = jsonr.get("location")["name"]

            weather["country"] = jsonr.get("location")['country']
            # if weather["country"] == "United States of America" or weather["country"] == "USA United States of America":
            #     weather["country"] = "United States"
            if weather["country"].find("United States") > -1:
                weather["country"] = "United States"

            weather["datetime"] = jsonr.get("location")['localtime']

            weather["temp_c"] = jsonr.get("current")['temp_c']
            weather["temp_f"] = jsonr.get("current")['temp_f']
            weather["feelslike_c"] = jsonr.get("current")['feelslike_c']
            weather["feelslike_f"] = jsonr.get("current")['feelslike_f']
            weather["humidity"] = jsonr.get("current")['humidity']

            weather["condition_text"] = jsonr.get("current")['condition']['text']
            weather["condition_icon"] = "https:" + jsonr.get("current")['condition']['icon']

            weather["max_temp_c"] = jsonr.get("forecast")['forecastday'][0]['day']['maxtemp_c']
            weather["min_temp_c"] = jsonr.get("forecast")['forecastday'][0]['day']['mintemp_c']
            weather["max_temp_f"] = jsonr.get("forecast")['forecastday'][0]['day']['maxtemp_f']
            weather["min_temp_f"] = jsonr.get("forecast")['forecastday'][0]['day']['mintemp_f']
            weather["sunrise"] = jsonr.get("forecast")['forecastday'][0]['astro']['sunrise']
            weather["sunset"] = jsonr.get("forecast")['forecastday'][0]['astro']['sunset']
            weather["moon_phase"] = jsonr.get("forecast")['forecastday'][0]['astro']['moon_phase']
            # print(weather)
            return weather

        except Exception as e:
            return False
        finally:
            pass