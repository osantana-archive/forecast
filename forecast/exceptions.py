# coding: utf-8

# Core Exceptions


class ForecastError(Exception):
    errno = 1

    def __init__(self, *args, **kwargs):
        self.errno = kwargs.pop("errno", 1)
        super(ForecastError, self).__init__(*args, **kwargs)


class SettingsError(ForecastError):
    pass


class ApplicationError(ForecastError):
    pass


class CommandError(ForecastError):
    pass


class MiddlewareError(ForecastError):
    pass
