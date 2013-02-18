# coding: utf-8


from __future__ import print_function

from forecast.exceptions import ForecastError
from forecast.manager import BaseCommand, Argument


class TestCommand(BaseCommand):
    help = "Run nosetest in installed applications"
    parameters = (
        Argument("--include-forecast", action="store_true", default=False),
    )

    def run(self, project, args, unknown_args):
        try:
            import nose  # pylint: disable-msg=F0401

            argv = ["discover"]

            print("Running tests for:")

            if args.include_forecast:
                print("   forecast")
                argv.append("forecast")

            for application in project.applications.keys():
                if application.startswith("forecast."):
                    continue

                argv.append(application)
                print("   %s" % (application,))

            print()

            argv.extend(unknown_args)
            nose.main(argv=argv)

        except ImportError:
            raise ForecastError("nosetests required for test running.")
