# coding: utf-8


import os
import sys

from forecast.exceptions import ForecastError


class Environment(object):
    def __init__(self, environment=None, base_list=None):
        self._current = environment

        if base_list is None:
            base_list = ["settings.base"]

        self._base_list = base_list

    @property
    def current(self):
        if self._current is not None:
            return self._current

        environment = os.environ.get("FORECAST_ENVIRONMENT", "base")

        for arg in sys.argv:
            if arg.startswith("--environment"):
                if "=" not in arg:
                    raise ForecastError("Invalid environment argument. Use --environment=NAME.")
                environment = (arg.rsplit("=", 1)[-1]) or "base"
                break

        return environment

    def get_settings(self):
        settings = self._base_list

        if self.current != "base":
            settings.append("settings.%s" % (self.current,))

        return settings
