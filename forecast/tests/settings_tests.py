# coding: utf-8


from unittest import TestCase
from forecast.environment import Environment

from forecast.exceptions import SettingsError
from forecast.settings import Settings


class SettingsTest(TestCase):
    def get_settings(self, environment="base"):
        env = Environment(environment)
        return Settings(env.get_settings(), _prefix="forecast.tests.")

    def test_base_setting_loading(self):
        settings = self.get_settings()
        self.assertEqual("forecast.tests.settings.base", settings["name"])

    def test_dev_setting_loading(self):
        settings = self.get_settings("dev")
        self.assertEqual("forecast.tests.settings.dev", settings["name"])

    def test_load_specific_settings(self):
        settings = self.get_settings("dev")
        settings.load()
        self.assertIn("forecast.tests.settings.dev", settings.loaded)

    def test_fail_load_unknown_settings(self):
        settings = self.get_settings("unknown")
        self.assertRaises(SettingsError, settings.load)

    def test_fail_load_invalid_settings(self):
        settings = self.get_settings("invalid")
        self.assertRaises(SettingsError, settings.load) # does not define SETTINGS={}
