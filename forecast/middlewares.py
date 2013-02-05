# coding: utf-8
from forecast.exceptions import MiddlewareError

from .signals import start_request, end_request, middleware_failure


class Middlewares(list):
    def __init__(self, settings, *args, **kwargs):
        self.settings = settings
        super(Middlewares, self).__init__(*args, **kwargs)

    def register(self, middlewares):
        for middleware in middlewares:
            instance = middleware(self.settings)
            self.append(instance)


class MiddlewareContextManager(object):
    def __init__(self, handler):
        self.handler = handler

    def __enter__(self):
        start_request.send(self.handler)

        middlewares = self.handler.middlewares
        for middleware in middlewares:
            try:
                middleware.start_request(self.handler)
            except Exception, error:
                middleware_failure.send(error)
                raise MiddlewareError("Error in middleware start %s: %s" % (middleware, error))

    def __exit__(self, exc_type, exc_val, exc_tb):
        middlewares = self.handler.middlewares
        for middleware in middlewares:
            try:
                middleware.end_request(self.handler)
            except Exception, error:
                middleware_failure.send(error)
                raise MiddlewareError("Error in middleware end %s: %s" % (middleware, error))

        end_request.send(self.handler)


class BaseMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    def start_request(self, handler):
        pass  # Do nothing!

    def end_request(self, handler):
        pass  # Do nothing!
