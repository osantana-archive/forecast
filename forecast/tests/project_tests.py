# coding: utf-8


import sys

from forecast.environment import Environment
from forecast.exceptions import ForecastError, SettingsError
from forecast.settings import Settings

from .core_tests import CoreTest


class ProjectTest(CoreTest):
    def test_required_core_app(self):
        env = Environment("base")
        settings = Settings(env.get_settings(), _prefix="forecast.tests.")
        project = self.get_project(settings=settings)
        project.install_applications()
        self.assertIn("forecast.applications.core", project.applications)

    def test_fail_install_unknown_application(self):
        project = self.get_project()
        self.assertRaises(ForecastError, project.install_application, "forecast.tests.unknown")

    def test_ignore_load_application_twice(self):
        project = self.get_project()
        project.install_application("forecast.tests.test_app")
        project.install_application("forecast.tests.test_app")
        self.assertEqual(1, len(project.applications))

    def test_install_applications_in_settings(self):
        environment = Environment()
        settings = Settings(environment.get_settings(), _prefix="forecast.tests.")
        project = self.get_project(settings=settings)
        project.install_applications()
        self.assertIn("forecast.tests.test_app", project.applications)

    def test_fail_incorrect_application_spec_in_settings(self):
        env = Environment("invalid_app_spec")
        settings = Settings(env.get_settings(), _prefix="forecast.tests.")
        project = self.get_project(settings=settings)
        self.assertRaises(SettingsError, project.install_applications)

    def test_run_dummy_command_in_project(self):
        environment = Environment()
        settings = Settings(environment.get_settings(), _prefix="forecast.tests.")
        project = self.get_project(settings=settings)

        argv = sys.argv
        sys.argv = ["./manage.py", "cmd"]
        self.assertEqual("ok", project.run())
        sys.argv = argv

    def test_tornado_app_settings(self):
        env = Environment("base")
        settings = Settings(env.get_settings(), _prefix="forecast.tests.")
        project = self.get_project(settings=settings)
        project.install_applications()
        app = project.get_tornado_application()
        self.assertIn("debug", app.settings)
