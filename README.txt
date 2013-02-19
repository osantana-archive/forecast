forecast:tornado
================
:Revision: draft

|build_status|

Forecast:tornado is a wrapper around Tornado web server that makes easy to
organize your projects "forcing" some package standards.

Installation
------------

Forecast:tornado requires the following packages:

* `Tornado`_ 2.4 or newer
* `Blinker`_ 1.2 or newer

Install from sources::

    $ python setup.py install

Or from PyPI (using pip)::

    $ pip install forecast

You can install the current development release::

    $ pip install -e git+https://github.com/osantana/forecast.git#egg=forecast-dev


Running tests
-------------

You can run forecast:tornado tests with the following command::

    $ python setup.py test


Terminology
-----------

A forecast:tornado project uses the following terminology:

project
    A forecast:tornado project is a directory containing a ``manage.py`` script
    file and a ``settings`` package containing the project configuration for
    various environments.

environment
    A project can run in several environments like *base*, *production*,
    *test*, *integration*, *dev*, etc. You can define a set of settings for
    each environment. When you start a forecast:tornado project it will load
    the default settings from forecast:tornado package, then these settings
    will be overriden by settings contained in ``settings.base`` module of your
    project and, at the end, by the settings in ``settings.{ENVIRONMENT}`` module.

application
    An application is a standard Python package containing an ``Application``
    class in it ``__init__.py``. You need to specify which applications you
    will use in environment's settings.

routes
    An URL mapping containing routes in format URLs ->
    ``tornado.web.RequestHandler``

middleware
    A forecast:tornado application could install middlewares in a project. The
    middlewares are executed before and after the ``RequestHandler.method()``
    associated with the requested ÙRL. They are useful for implementing
    orthogonal functionality in projects (eg. database connections).

signals
    Forecast:tornado uses `Blinker`_ library to send and handle signals in a
    project.


Starting a Project
------------------

Let's start a project from scratch. Our project will be called ``rainning`` and
it will return a JSON-serialized object of the weather forecast for 'today' or
'tomorrow'.

Before we start our project lets create a ``virtualenv``::

    $ virtualenv rainning
    $ cd rainning
    $ source bin/activate
    (rainning) $

Now we can install the development version of forecast:tornado::

    $ pip install -e git+https://github.com/osantana/forecast.git#egg=forecast-dev
    ... installing forecast and its dependencies ...

Forecast:tornado it creates a script called ``forecast`` that we can use to
start our project::

    $ forecast start --skel=project rainning
    $ ls rainning
    __init__.py      manage.py        requirements.txt settings

Now we've a basic project to start with::

    $ cd rainning
    $ python manage.py runserver

You can point your browse to http://localhost:8888/ and you can see a random
text about the 'weather'.

Now it's time to start a application where we'll handle the requests::

    $ python manage.py start --skel=application willitrain
    $ ls willitrain
    __init__.py    controllers.py routes.py

We've created an application based on a skel bundled with forecast:tornado.
It's time to install this application in our project. Let's add the following
line in our ``settings/base.py`` file:

.. code-block:: python

    SETTINGS = {
        "name": "settings.base",
        "applications": (
            "willitrain",
        ),
        "location": 455827, # We will use this code below. (Sao Paulo, BR - http://woeid.rosselliot.co.nz/lookup)
    }

We can install an application adding the package name in ``applications``
settings (above) or we can specify a tuple containing the applications' package
name and a ``base_url`` that will be prepended to every route defined by our
application:

.. code-block:: python

    SETTINGS = {
        "name": "settings.base",
        "applications": (
            ("willitrain", r"/willitrain"),
        ),
        "location": 455827, # We will use this code below. (Sao Paulo, BR - http://woeid.rosselliot.co.nz/lookup)
    }

Let's define a default route for "/willitrain/" URL in ``willitrain/routes.py``:

.. code-block:: python

    from forecast.routes import Route
    from .controllers import IndexHandler

    routes = (
        Route(r"^(?P<when>today|tomorrow)/?$", IndexHandler, name="index"),
    )

Now, we will implement a handler that will get the forecast for a location
(specified in settings) using `Yahoo! Weather API`_:

.. code-block:: python

    from xml.dom import minidom
    from datetime import datetime, timedelta
    from urllib import urlencode

    from tornado.web import HTTPError, asynchronous
    from tornado.httpclient import AsyncHTTPClient
    from tornado.gen import engine, Task

    from forecast.web import RequestHandler


    class IndexHandler(RequestHandler):
        @asynchronous
        @engine
        def get(self, when):
            date = datetime.now()
            if when == "tomorrow":
                date += timedelta(1)

            date_string = datetime.strftime(date, "%d %b %Y")
            woeid = urlencode({"w": self.settings["location"]})  # WOEID defined in settings/base.py

            # Use Yahoo! Weather API: http://developer.yahoo.com/weather/
            url = "http://weather.yahooapis.com/forecastrss?" + woeid
            http_client = AsyncHTTPClient()
            response = yield Task(http_client.fetch, url)

            xmldoc = minidom.parseString(response.body)
            elements = xmldoc.getElementsByTagName("yweather:forecast")

            for element in elements:
                if element.getAttribute("date") == date_string:
                    self.write({"date": date_string, "text": element.getAttribute("text"), "code": element.getAttribute("code")})
                    break

            else:  # date not found
                self.write({"date": date_string, "text": "not available", "code": "3200"})

            self.finish()

We use the Tornado's asynchronous API to avoid block the Web server until we
get the response from Yahoo! Weather API.


.. |build_status| image:: https://secure.travis-ci.org/osantana/forecast.png?branch=master
   :target: https://travis-ci.org/osantana/forecast
.. _Tornado: http://www.tornadoweb.org/
.. _Blinker: http://discorporate.us/projects/Blinker/
.. _Yahoo! Weather API: http://developer.yahoo.com/weather/


