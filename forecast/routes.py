# coding: utf-8


from collections import OrderedDict, Iterable

from tornado.web import URLSpec


class Route(object):
    def __init__(self, pattern, handler, args=None, name=None):
        self.pattern = pattern
        self.handler = handler
        self.name = name
        self.args = args

    def get_url_pattern(self, base_url=""):
        pattern = self.pattern

        base_url = base_url.strip("^$/") # filter base_url metachars and slashes
        if base_url:
            pattern = r"%s/%s" % (r"^/" + base_url, self.pattern.strip("^$").lstrip("/"))

        if not pattern.endswith("$"):
            pattern += "$"

        return pattern

    def get_url_spec(self, base_url=""):
        pattern = self.get_url_pattern(base_url)
        return URLSpec(pattern, self.handler, self.args, name=self.name)


class Routes(object):
    def __init__(self, settings):
        self.settings = settings
        self.map = OrderedDict()

    def register(self, routes, base_url=""):
        if not isinstance(routes, Iterable):
            routes = (routes,)

        for route in routes:
            self.map[route.get_url_pattern(base_url)] = (route, base_url)

    def get_urlspecs(self):
        return [route.get_url_spec(base_url) for route, base_url in self.map.values()]
