# coding: utf-8


from forecast.manager import BaseCommand


class CmdCommand(BaseCommand):
    def run(self, project, args, unknown_args):
        return "ok"
