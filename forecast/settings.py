# coding: utf-8

from collections import OrderedDict
from copy import deepcopy

from forecast.utils import import_object
from forecast.exceptions import SettingsError
from forecast.defaults import DEFAULT_SETTINGS


class Settings(object):
    def __init__(self, settings_list, _prefix=""):
        self.settings_list = settings_list
        self._prefix = _prefix

        self.settings = deepcopy(DEFAULT_SETTINGS)
        self.loaded = OrderedDict()

    def load(self):
        for settings_path in self.settings_list:
            name = self._prefix + settings_path
            settings = self._import_settings(name)

            settings['name'] = name
            self.loaded[name] = settings

            self.settings.update(settings)

    def _import_settings(self, path):
        try:
            _, settings = import_object("%s.SETTINGS" % (path,))
        except ImportError, ex:
           raise SettingsError("Error importing %s.SETTINGS (%s)" % (path,ex))

        return settings

    def __getitem__(self, key):
        if not self.loaded:
            self.load()

        return self.settings[key]

    def get(self, key, default=None):
        if not self.loaded:
            self.load()

        return self.settings.get(key, default)
