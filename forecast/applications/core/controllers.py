# coding: utf-8


from random import choice

from forecast.web import RequestHandler


class ItWorkedHandler(RequestHandler):
    def get(self):
        hello = ["Ride the thunder!",
                 "Bring the thunder!",
                 "Make it rain"]
        self.write(choice(hello))
