# coding: utf-8
import sys

from forecast.environment import Environment
from forecast.manager import Manager, BaseCommand
from forecast.settings import Settings

from forecast.tests.core_tests import CoreTest


class DummyCommand(BaseCommand):
    name = "dummy"

    def run(self, project, args, unknown_args):
        return "ok"


class EmptyCommand(BaseCommand):  # pylint: disable-msg=W0223
    pass


class DummyProject(object):
    pass


class ManagerTest(CoreTest):
    def get_manager(self):
        env = Environment()
        settings = Settings(env.get_settings(), _prefix="forecast.tests.")
        return Manager(settings)

    def test_command_registration(self):
        manager = self.get_manager()
        manager.register(DummyCommand())
        self.assertIn("dummy", manager.commands)

    def test_run_dummy_command(self):
        manager = self.get_manager()
        manager.register(DummyCommand())
        self.assertEquals("ok", manager.run(DummyProject(), argv=["dummy"]))

    def test_register_empty_command_same_module_name(self):
        manager = self.get_manager()
        manager.register(EmptyCommand())
        self.assertIn("manager_tests", manager.commands)

    def test_fail_run_empty_command(self):
        manager = self.get_manager()
        manager.register(EmptyCommand())
        self.assertRaises(NotImplementedError, manager.run, DummyProject(), argv=["manager_tests"])

    def test_run_dummy_command_using_argv(self):
        manager = self.get_manager()
        manager.register(DummyCommand())

        argv = sys.argv
        sys.argv = ["./manage.py", "dummy"]
        self.assertEqual("ok", manager.run(DummyProject()))
        sys.argv = argv
