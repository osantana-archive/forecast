# coding: utf-8


from forecast.web import RequestHandler

from random import choice


class HelloWorldHandler(RequestHandler):
    def get(self):
        hello = ["Ride the thunder!",
                 "Bring the thunder!",
                 "Make it rain"]
        self.write(choice(hello))
