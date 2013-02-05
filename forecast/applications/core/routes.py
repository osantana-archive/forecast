# coding: utf-8


from forecast.routes import Route

from .controllers import ItWorkedHandler


routes = (
    Route(r"^/$", ItWorkedHandler, name="it-worked"),
)
