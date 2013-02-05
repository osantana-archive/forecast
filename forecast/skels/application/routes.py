# coding: utf-8


from forecast.routes import Route

from .controllers import HelloWorldHandler


routes = (
    Route(r"^/$", HelloWorldHandler, name="hello-world"),
)
