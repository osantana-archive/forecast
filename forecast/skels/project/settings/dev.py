# coding: utf-8


from forecast.skels.project.settings.base import SETTINGS as settings


SETTINGS = {
    "name": "settings.dev",
    "applications": settings["applications"] + (
#        "debugging",
    ),
}
