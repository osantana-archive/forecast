#!/usr/bin/env python
# coding: utf-8
# pragma: no cover


import sys

from forecast.exceptions import ForecastError
from forecast.environment import Environment
from forecast.project import Project


def main():
    environment = Environment(base_list=[])
    project = Project(environment=environment)
    try:
        project.run()
    except ForecastError, ex:
        import traceback
        traceback.print_exc()
        sys.exit(ex.errno)


if __name__ == '__main__':
    main()
