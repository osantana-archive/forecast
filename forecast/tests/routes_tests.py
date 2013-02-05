# coding: utf-8


import re
from unittest import TestCase

from tornado.web import RequestHandler
from forecast.environment import Environment

from forecast.routes import Route, Routes
from forecast.settings import Settings


class DummyHandler(RequestHandler):
    pass


class RoutesTest(TestCase):
    def get_routes(self):
        env = Environment()
        settings = Settings(env.get_settings(), _prefix="forecast.tests.")
        return Routes(settings)

    def test_empty_routing_table(self):
        routes = self.get_routes()
        self.assertEqual(0, len(routes.map))

    def test_register_basic_route(self):
        routes = self.get_routes()
        routes.register(Route("/foo", DummyHandler))
        self.assertIn(r"/foo$", routes.map)

    def test_register_basic_route_with_baseurl(self):
        routes = self.get_routes()
        routes.register(Route("/foo", DummyHandler), base_url="base")
        self.assertIn(r"^/base/foo$", routes.map)

    def test_register_two_routes(self):
        routes = self.get_routes()
        routes.register(Route("/foo", DummyHandler))
        routes.register(Route("/bar", DummyHandler), base_url="/base/")
        self.assertIn(r"/foo$", routes.map)
        self.assertIn(r"^/base/bar$", routes.map)

    def test_register_two_routes_equals(self):
        routes = self.get_routes()
        routes.register(Route("^/base/foo$", DummyHandler, name="first"))
        routes.register(Route("/foo", DummyHandler, name="last"), base_url="base")
        self.assertIn(r"^/base/foo$", routes.map)
        self.assertEqual("last", routes.map[r"^/base/foo$"][0].name)
        self.assertEquals(1, len(routes.map))

    def test_urlspecs(self):
        routes = self.get_routes()
        routes.register(Route("^/foo/1$", DummyHandler, name="first"))
        routes.register(Route("^/foo/2$", DummyHandler, name="second"))
        routes.register(Route("^/foo/3$", DummyHandler, name="third"))
        routes.register(Route("^/foo/4$", DummyHandler, name="fourth"))
        routes.register(Route("^/foo/4$", DummyHandler, name="last"))

        urlspecs = routes.get_urlspecs()
        self.assertEqual("first", urlspecs[0].name)
        self.assertEqual("second", urlspecs[1].name)
        self.assertEqual("third", urlspecs[2].name)
        self.assertEqual("last", urlspecs[3].name)


class RouteTest(TestCase):
    def assertUrlSpecPattern(self, urlspec, pattern):
        from_re = urlspec.regex.pattern
        to_re = re.compile(pattern).pattern
        self.assertEqual(from_re, to_re)

    def assertUrlPattern(self, url, pattern, base_url=""):
        urlspec = url.get_url_spec(base_url)
        self.assertUrlSpecPattern(urlspec, pattern)

    def test_basic_route_urlspec(self):
        patterns = (
            (r"/foo", r"/foo$", ""),
            (r"/foo$", r"/foo$", ""),
            (r"/foo/", r"/foo/$", ""),
            (r"/foo", r"^/base/foo$", r"/base"),
            (r"/foo", r"^/base/foo$", r"base"),
            (r"/foo/", r"^/base/foo/$", r"/base/"),
            (r"^/foo/$", r"^/base/foo/$", r"/base/"),
            (r"/foo/$", r"^/base/foo/$", r"/base/$"),
            (r"foo/$", r"^/base/foo/$", r"/base/$"),
            (r"//foo/$", r"^/base/foo/$", r"^//base//$"),
            (r"^/foo/$", r"^/foo/$", r"/"),
            (r"^/foo/$", r"^/foo/$", r"^/"),
            (r"^/foo/$", r"^/foo/$", r"^/$"),
        )

        for urlpattern, urlspecpattern, base_url in patterns:
            url = Route(urlpattern, DummyHandler)
            self.assertUrlPattern(url, urlspecpattern, base_url)

    def test_urlspec_attributes(self):
        route = Route(r"/foo", DummyHandler, {"template": "foo.html"}, name="foo-route")
        urlspec = route.get_url_spec(r"/base")
        self.assertEqual(r"^/base/foo$", urlspec.regex.pattern)
        self.assertEqual("foo-route", urlspec.name)
        self.assertIs(DummyHandler, urlspec.handler_class)
        self.assertIn("template", urlspec.kwargs)
