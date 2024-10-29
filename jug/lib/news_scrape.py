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


    def get_news_rss(self):
        # // 2024-10-29 Tue 03:25
        # Yahoo rss suddenly stopped working!!!

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

    def get_news(self):

        url = "https://www.yahoo.com/news/world/"
        base_url = "https://www.yahoo.com"

        response = self.send_req(url)
        # logger.info(f'Yahoo reqs: {response.text}')

        html = response.text

        linkList = []
        headlineList = []
        html_start = 0
        y = 0

        for _ in range(7):

            html = html[html_start+y:]
            html_start = html.find("data-ylk=\"itc:0;elm:hdln;elmt:")
            html_end = html_start + 2000

            if html_start < 0:
                break

            section = html[html_start:html_end]

            x = section.find("href=")
            section = section[x+6:]
            x = section.find(">")

            link = section[:x-1]
            if link.find("https://") == 0 and link.find(base_url) != 0:
                # Sometimes, randomly, gets strange sports ad and screws up the parsing;
                # But can't replicate it on demand; yahoo seems to insert it randomly;
                # Its base url is not yahoo.news but sports something;
                # print("bad news page")
                # print(html)
                self.get_news()
                break

            if link.find(base_url) != 0:
                link = base_url + link

            linkList.append(link)

            section = section[x+1:]
            y = section.find("<")


            headline = section[:y]
            # decode html characters back to normal;
            # But this also seems to make headilne into type Beautifulsoup
            # So have to convert back to text, or else get error when trying to jsonify later;
            headline = BeautifulSoup(headline, "html.parser")
            headlineList.append(headline.text)

        # print(headlineList)
        # print(linkList)

        soup2 = []
        for idx in range(len(headlineList)):
            soup2.append([headlineList[idx], linkList[idx]])

        self.result = soup2


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
