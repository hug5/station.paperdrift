from flask import Flask, render_template, request
from datetime import datetime


class Home:

    def __init__(self):

        self.dateTimeN = datetime.now().date()
        self.dayNameIndex = int(self.dateTimeN.strftime('%w'))
        self.dayNameList = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        self.doHome()

    def doHome(self):
        self.name = "Bobby"
        self.age = 21
        self.location = "Miami"
        self.dayName = self.dayNameList[self.dayNameIndex]
        self.now = self.dateTimeN
        self.user_agent = request.headers.get('User-Agent'),

    def mult(self, arg):
        return arg*3


homeobj = Home()


from jug.html import homeHtml
result = homeHtml.HomeHtml.doHtml(obj)

