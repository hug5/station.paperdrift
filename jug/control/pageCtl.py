from jug.lib.logger import logger
from flask import render_template
from jug.lib.f import F


class PageCtl():

    def __init__(self):

        self.article = ''
        self.header = ''
        self.footer = ''
        self.logo = ''

        self.html = ''

    def getHtml(self):
        return self.html

    def doCommon(self):
        from jug.control.headerCtl import HeaderCtl
        from jug.control.footerCtl import FooterCtl

        logger.info('DoCommon')

        def doHeader():
            obj = HeaderCtl()
            obj.start()
            self.header = obj.getHtml()

        def doFooter():
            obj = FooterCtl()
            obj.start()
            self.footer = obj.getHtml()

        def doLogo():
            self.logo = render_template(
                "logo.jinja"
            )

        doHeader()
        doFooter()
        doLogo()
        # pass

    def doHome(self):
        from jug.control.homeCtl import HomeCtl

        logger.info('DoHome')
        # F.uwsgi_log("doHome")


        self.doCommon()

        home_obj = HomeCtl()
        # self.article = home_obj.start()
        home_obj.start()

        self.article = home_obj.getHtml()
        site_title = home_obj.getConfig()["site_title"]

        html = render_template(
            "pageHtml.jinja",
            title = site_title,
            header = self.header,
            article = self.article,
            footer = self.footer,
            # db = dbc
        )

        # return F.stripJinja(html) + self.logo
        self.html = F.stripJinja(html) + self.logo


    def doSomePathUrl(self, url):
        from jug.control import pathCtl

        logger.info('DoSomePathUrl')

        self.doCommon()

        pathO = pathCtl.PathCtl(url)
        self.article = pathO.start()
        site_title = pathO.getConfig()["site_title"]


        html = render_template(
            "pageHtml.jinja",
            title = site_title,
            header = self.header,
            article = self.article,
            footer = self.footer,
        )

        self.html = F.stripJinja(html) + self.logo