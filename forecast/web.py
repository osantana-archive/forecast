# coding: utf-8


import tornado.web

from .exceptions import MiddlewareError
from .middlewares import MiddlewareContextManager


class RequestHandler(tornado.web.RequestHandler):
    def __init__(self, tornado_application, request, **kwargs):
        self._project = tornado_application.project
        super(RequestHandler, self).__init__(tornado_application, request, **kwargs)

    @property
    def middlewares(self):
        return self._project.middlewares

    @property
    def settings(self):
        return self._project.settings

    def _execute(self, *args, **kwargs):
        try:
            with MiddlewareContextManager(self):
                return super(RequestHandler, self)._execute(*args, **kwargs)  # pylint: disable-msg=W0212
        except MiddlewareError, ex:
            raise tornado.web.HTTPError(500, log_message=str(ex))
