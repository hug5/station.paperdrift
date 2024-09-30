import requests
import json
import random


class Weather_api:

    def __init__(self):
        pass

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
            "Tokyo",
            "Seoul",
            "Ulaanbaatar",
            "Paris",
            "London",
            "Los Angeles",
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


    def call_weather(self, location):
        w_url = "https://api.weatherapi.com/v1/current.json?key=d15ec96bdfd048c0bda84905243009&aqi=no&q="
        # location="Los Angeles"
        url = w_url + location
        # response = send_req(url)
        # print(response.text)
        jsonr = json.loads(self.send_req(url).text)

        return jsonr

    def do_weather(self, location):

        jsonr = self.call_weather(location)

        # If bad location, then get will default to None
        # result = jsonr.get("location", "other_default_value")
        result = jsonr.get("location")

        while result is None:
            # If bad location, then try random location:
            jsonr = self.call_weather(self.get_random_location())
            result = jsonr.get("location")

        # parse the json
        # Remember that the location may be fake; ie, not match with request;
        try:

            weather = {}

            # Parse json:
            # city = jsonr.get("location['name']", "error")
            weather["location"] = jsonr.get("location")["name"]

            weather["country"] = jsonr.get("location")['country']
            weather["datetime"] = jsonr.get("location")['localtime']

            weather["temp_c"] = jsonr.get("current")['temp_c']
            weather["temp_f"] = jsonr.get("current")['temp_f']
            weather["feelslike_c"] = jsonr.get("current")['feelslike_c']
            weather["feelslike_f"] = jsonr.get("current")['feelslike_f']
            weather["humidity"] = jsonr.get("current")['humidity']

            weather["condition_text"] = jsonr.get("current")['condition']['text']
            weather["condition_icon"] = "https:" + jsonr.get("current")['condition']['icon']

            # print(weather)
            return weather

        except Exception as e:
            return False
        finally:
            pass