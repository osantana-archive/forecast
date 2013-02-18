# coding: utf-8


from forecast.routes import Route

from .controllers import IndexHandler


routes = (
    Route(r"^/$", IndexHandler, name="index"),
)
