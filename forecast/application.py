# coding: utf-8


from forecast.exceptions import ApplicationError

from forecast.utils import import_object, package_contents, camelize


class BaseApplication(object):
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings

    @property
    def package_name(self):
        return self.__module__

    @property
    def routes(self):
        urlpatterns = "%s.routes.routes" % (self.package_name,)
        try:
            _, routes = import_object(urlpatterns)
        except ImportError, ex:
            raise ApplicationError("Error reading routing table from %s: %s" % (urlpatterns, ex))

        try:
            routes = tuple(routes)
        except TypeError:
            raise ApplicationError("Invalid routing table %r (it's not a sequence of Routes() objects)." % (routes,))

        return routes

    @property
    def commands(self):
        ret = []

        try:
            commands = package_contents("%s.commands" % (self.package_name,), filter_function=lambda name: name.startswith("_"))
        except ImportError:
            return ret

        for command in commands:
            class_name = "%sCommand" % (camelize(command))
            _, cmdclass = import_object("%s.commands.%s.%s" % (self.package_name, command, class_name))
            ret.append(cmdclass())

        return ret

    @property
    def middlewares(self):
        return ()
