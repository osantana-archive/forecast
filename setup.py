import os
from distutils.core import setup

path = os.path.dirname(__file__)

setup(
    name='forecast',
    version='0.1',
    author="Osvaldo Santana Neto",
    author_email="forecast@osantana.me",
    packages=[
        'forecast',
        'forecast.applications',
        'forecast.applications.core',
        'forecast.applications.core.commands',
        'forecast.skels',
        'forecast.skels.application',
        'forecast.skels.project',
        'forecast.skels.project.settings',
        'forecast.tests',
        'forecast.tests.settings',
        'forecast.tests.test_app',
        'forecast.tests.test_app.commands',
    ],
    package_dir={
        'forecast.skels.project': os.path.join(path, 'forecast', 'skels', 'project'),
    },
    package_data={
        'forecast.skels.project': [
            'requirements.txt',
        ],
    },
    scripts=[
        os.path.join(path, 'bin', 'forecast-admin.py'),
        os.path.join(path, 'bin', 'forecast')
    ],
    url="http://github.com/osantana/forecast",
    license='MIT',
    description="A small wrapper around Tornado Web Server to force project structure",
    long_description=open(os.path.join(path, 'README.txt')).read(),
)

