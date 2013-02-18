# coding: utf-8


from forecast.web import RequestHandler


class IndexHandler(RequestHandler):
    def get(self):
        self.write("Index")
