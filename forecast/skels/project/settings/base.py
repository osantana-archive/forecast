# coding: utf-8
# pragma: no cover

from forecast.defaults import DEFAULT_SETTINGS as settings

SETTINGS = {
    "name": "settings.base",
    "applications": settings["applications"] + (
#        "main_app",
    ),
}
