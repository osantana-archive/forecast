# coding: utf-8


from unittest import TestCase

from forecast.utils import import_object, package_contents, camelize


class HelperFunctionsTest(TestCase):
    def test_import_object(self):
        module, imported_object = import_object("forecast.tests.settings.base.SETTINGS")
        self.assertTrue(repr(module).startswith("<module 'forecast.tests.settings.base' from"))
        self.assertIsInstance(imported_object, dict)

    def test_fail_import_invalid_module(self):
        self.assertRaises(ImportError, import_object, "forecast.tests.unknown")

    def test_fail_import_invalid_object(self):
        self.assertRaises(ImportError, import_object, "forecast.tests.settings.base.UNKNOWN")

    def test_package_contents(self):
        modules = package_contents("forecast.tests.test_app.commands")
        self.assertIn("cmd", modules)
        self.assertIn("__init__", modules)

    def test_fail_package_contents_in_module(self):
        self.assertRaises(ImportError, package_contents, "forecast.tests.test_app.commands.cmd")

    def test_fail_package_contents_with_non_packages(self):
        self.assertRaises(ImportError, package_contents, "forecast.tests.nonpackage")

    def test_camelize_names(self):
        self.assertEqual("Camel", camelize("camel"))
        self.assertEqual("CamelCase", camelize("camel_case"))
        self.assertEqual("CamelCaseFunctionTransformation", camelize("camel_case_function_transformation"))
        self.assertEqual("CamelCase", camelize("camel__case"))
