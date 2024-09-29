from jug.lib.logger import logger
# Making an HTTP Request
import requests
from bs4 import BeautifulSoup

class ReqsCtl():

    def __init__(self):
        pass

        #self.word = "smart"
        # syn_list = set{} # set
        #self.syn_list = set() # To create, have to use (), not {}; confusing!

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


    def get_yahoo_news(self):

        url = "https://news.yahoo.com/rss/world"

        response = self.send_req(url)

        # logger.info(f'reqs: {response.text}')

        soup = BeautifulSoup(response.text, 'xml')
          # Must have lxml to make this work:
          # $ pip install lxml

        # logger.info(f'reqs: {soup.text}')

        soup1 = soup.find_all('title')
        soup1_link = soup.find_all('link')

        soup2 = []
        soup2L = []


        # first 2 titles are yahoo site titles;
        for idx in range(2, len(soup1)):
            soup2.append(soup1[idx].text)
            soup2L.append(soup1_link[idx].text)

        return [soup2, soup2L]

        # print(soup2)
        # print(soup2L)


