# coding: utf-8


import os
import forecast

try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages


path = os.path.dirname(__file__)

with open("requirements.txt") as requirements:
    requires = requirements.readlines()

with open("README.txt") as readme:
    long_description = readme.read()

setup(
    name='forecast',
    version=forecast.__version__,
    url="http://github.com/osantana/forecast",
    license='MIT',
    author="Osvaldo Santana Neto",
    author_email="forecast@osantana.me",
    description="A small wrapper around Tornado Web Server to force project structure",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Tornado",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],

    zip_safe=False,
    platforms="any",
    packages=find_packages(exclude=""),
    include_package_data=True,
    install_requires=requires,
    package_dir={
        'forecast.skels.project': os.path.join(path, 'forecast', 'skels', 'project'),
    },
    package_data={
        'forecast.skels.project': ['requirements.txt'],
    },
    scripts=[os.path.join(path, 'bin', 'forecast')],
)

