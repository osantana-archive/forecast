# coding: utf-8


import os
import sys
from unittest import TestCase

from forecast.environment import Environment
from forecast.exceptions import ForecastError


class EnvironmentTests(TestCase):
    def test_base_environment(self):
        argv = sys.argv[:]
        sys.argv = []

        env = Environment()
        self.assertEquals("base", env.current)

        sys.argv = argv

    def test_dev_environment(self):
        env = Environment("dev")
        self.assertEquals("dev", env.current)

    def test_base_environment_settings(self):
        argv = sys.argv[:]
        sys.argv = []

        env = Environment()
        self.assertListEqual(["settings.base"], env.get_settings())

        sys.argv = argv

    def test_dev_environment_settings(self):
        env = Environment("dev")
        self.assertListEqual(["settings.base", "settings.dev"], env.get_settings())

    def test_select_environment_via_cli(self):
        sys.argv.append("--environment=dev")

        env = Environment()
        self.assertEquals("dev", env.current)

        sys.argv.pop()

    def test_select_environment_via_os_environment(self):
        os.environ["FORECAST_ENVIRONMENT"] = "dev"

        env = Environment()
        self.assertEqual("dev", env.current)

        del os.environ["FORECAST_ENVIRONMENT"]

    def test_select_environment_via_cli_ignoring_env(self):
        os.environ["FORECAST_ENVIRONMENT"] = "ignoring"
        sys.argv.append("--environment=dev")

        env = Environment()
        self.assertEqual("dev", env.current)

        del os.environ["FORECAST_ENVIRONMENT"]
        sys.argv.pop()

    def test_fail_wrong_environment_by_cli(self):
        argv = sys.argv[:]
        sys.argv = ["--environment-in-wrong-format"]

        try:
            assert not Environment().current
            self.fail("Must raise a ForecastError") # pragma: no cover
        except ForecastError:
            pass

        sys.argv = argv
