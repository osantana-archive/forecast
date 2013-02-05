# coding: utf-8


from collections import OrderedDict

import tornado.web

from .exceptions import ForecastError, SettingsError
from .middlewares import Middlewares
from .utils import import_object
from .environment import Environment
from .settings import Settings
from .manager import Manager
from .routes import Routes


class Project(object):
    def __init__(self, environment=None, settings=None, manager=None, routes=None, middlewares=None):
        self.environment = self._initialize(environment, Environment)

        settings_list = self.environment.get_settings()
        self.settings = self._initialize(settings, Settings, settings_list)

        self.manager = self._initialize(manager, Manager, self.settings)
        self.routes = self._initialize(routes, Routes, self.settings)
        self.middlewares = self._initialize(middlewares, Middlewares, self.settings)

        self.applications = OrderedDict()

    def _initialize(self, attribute, cls, *args, **kwargs):
        if attribute is None:
            return cls(*args, **kwargs)
        return attribute

    def install_application(self, application_package, base_url=""):
        if application_package in self.applications:
            return

        try:
            application_module, application_class = import_object("%s.Application" % (application_package,))
        except ImportError:
            raise ForecastError("%s.Application not found." % (application_package,))

        application = application_class(application_package, self.settings)

        self.routes.register(application.routes, base_url)
        self.manager.register(application.commands)
        self.middlewares.register(application.middlewares)

        self.applications[application_package] = application

    def install_applications(self):
        if "forecast.applications.core" not in self.applications:
            self.install_application("forecast.applications.core")

        for application in self.settings['applications']:
            if isinstance(application, basestring):
                application_path = application
                base_url = ""
            elif isinstance(application, (tuple,list)):
                application_path, base_url = application
            else:
                raise SettingsError("Invalid application spec: %r" % (application,))

            self.install_application(application_path, base_url)

    def run(self):
        if not self.applications:
            self.install_applications()

        return self.manager.run(self)

    def get_tornado_application(self):
        handlers = self.routes.get_urlspecs()
        settings = self.settings['tornado']
        return TornadoApplication(self, handlers=handlers, **settings)


class TornadoApplication(tornado.web.Application):
    def __init__(self, project, *args, **kwargs):
        self.project = project
        super(TornadoApplication, self).__init__(*args, **kwargs)
