# coding: utf-8


import sys
from unittest import TestCase

from forecast.project import Project


class CoreTest(TestCase):
    def get_project(self, *args, **kwargs):
        argv = sys.argv
        sys.argv = argv[:1]
        project = Project(*args, **kwargs)
        sys.argv = argv
        return project

