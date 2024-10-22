from jug.lib.logger import logger
# Making an HTTP Request
import requests
from bs4 import BeautifulSoup
import json


class News_Scrape():

    def __init__(self):

        #self.word = "smart"
        # syn_list = set{} # set
        #self.syn_list = set() # To create, have to use (), not {}; confusing!
        self.result = None

    def getResult(self):
        return self.result


    def send_req(self, url):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

        # Cookies and sessions?
        # response = requests.Session()

        response = requests.get(url, headers=headers, timeout=6)
        response.encoding = "utf-8"
        return response


    def get_news(self):

        url = "https://news.yahoo.com/rss/world"

        response = self.send_req(url)

        logger.info(f'Yahoo reqs: {response.text}')

        soup = BeautifulSoup(response.text, 'xml')
          # Must have lxml to make this work:
          # $ pip install lxml

        # logger.info(f'reqs: {soup.text}')

        soup1 = soup.find_all('title')
        soup1_link = soup.find_all('link')

        soup2 = []
        # soup2L = []

        # first 2 titles are yahoo site titles;
        for idx in range(2, len(soup1)):
            # soup2.append(soup1[idx].text)
            # soup2L.append(soup1_link[idx].text)

            # Conventional format now:
            soup2.append([soup1[idx].text, soup1_link[idx].text])

        # return [soup2, soup2L]
        # return soup2
        self.result = soup2


        # Format: So not what you might expect;
        # This gives us flexibility if we only want to grab the headlines;
        # [ ["h1", "h2", "h3"], ["url1", "url2", "url3"] ]


        # print(soup2)
        # print(soup2L)

    def get_britannica(self, location):

        # location = "Miami"

        url = 'https://www.britannica.com/search?query='
        response = self.send_req(f'{url}{location}')

        soup = BeautifulSoup(response.text, 'html.parser')


        # Find the specific script tag
        script_tag = soup.find('script', {'data-type': 'Init Mendel'})

        if not script_tag:
            logger.info(f'britannica not found: {location}')
            return False

        json_result = {}

        try:

            resultStart = script_tag.text.find("topicInfo")
            resultStart += 11

            resultEnd = script_tag.text.find("toc", resultStart)
            resultEnd -= 2

            result = script_tag.text[resultStart:resultEnd]

            json_result = json.loads(result)
            self.result = json_result
            # return json_result

            # print(json_result["title"])
            # print(json_result["url"])
            # print(json_result["description"])
            # print(json_result["imageUrl"])

        except Exception as e:
            logger.info(f"Britannica error: {e}")
            self.result = {}
