from jug.lib.logger import logger
from flask import render_template
from jug.lib.f import F
from jug.control.headerCtl import HeaderCtl
from jug.control.footerCtl import FooterCtl


class PageCtl():

    def __init__(self):

        self.article = ''
        self.header = ''
        self.footer = ''
        self.ascii_art = ''

        self.html = ''

    def getHtml(self):
        return self.html

    def doHeader(self):
        ob = HeaderCtl()
        ob.start()
        self.header = ob.getHtml()

    def doFooter(self):
        ob = FooterCtl()
        ob.start()
        self.footer = ob.getHtml()

    def doAscii_art(self):
        self.ascii_art = render_template(
            "ascii_art.jinja"
        )

    def doCommon(self):
        # logger.info('DoCommon')
        self.doHeader()
        self.doFooter()
        self.doAscii_art()
        # pass

    def doHome(self):
        from jug.control.homeCtl import HomeCtl

        logger.info('DoHome')
        # F.uwsgi_log("doHome")


        self.doCommon()

        ob = HomeCtl()
        # self.article = ob.start()
        ob.start()

        self.article = ob.getHtml()
        site_title = ob.getConfig()["site_title"]

        html = render_template(
            "pageHtml.jinja",
            title = site_title,
            header = self.header,
            article = self.article,
            footer = self.footer,
            # db = dbc
        )

        logger.info(f'---type info: {type(html)}')
        self.html = F.stripJinja(html) + self.ascii_art
        # self.html = html + self.ascii_art


    def doSomePathUrl(self, url):
        from jug.control.pathCtl import PathCtl

        logger.info('DoSomePathUrl')

        self.doCommon()

        ob = PathCtl(url)
        # self.article = ob.start()
        ob.start()
        self.article = ob.getHtml()
        site_title = ob.getConfig()["site_title"]

        html = render_template(
            "pageHtml.jinja",
            title = site_title,
            header = self.header,
            article = self.article,
            footer = self.footer,
        )

        self.html = F.stripJinja(html) + self.ascii_art
        # self.html = html + self.ascii_art