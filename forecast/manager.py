# coding: utf-8


import sys
import argparse
import collections


class Manager(object):
    def __init__(self, settings):
        self.settings = settings
        self.commands = {}

        self._parser = argparse.ArgumentParser()
        self._commands_parser = self._parser.add_subparsers(dest="command", help="commands available")
        self._parser.add_argument("--environment", action="store", default="base")

    def register(self, commands):
        if not isinstance(commands, collections.Iterable):
            commands = (commands,)

        for command in commands:
            self.commands[command.name] = command

            subparser = self._commands_parser.add_parser(command.name, help=command.help_text)

            for parameter in command.parameters:
                subparser.add_argument(*parameter.args, **parameter.kwargs)

    def run(self, project, argv=None):
        if argv is None:
            argv = sys.argv[1:]
        args, unknown_args = self._parser.parse_known_args(argv)
        command = self.commands[args.command]
        return command.run(project, args, unknown_args)


class BaseCommand(object):
    help_text = ""
    parameters = ()

    def __init__(self):
        self._module_name = self.__module__.split(".")[-1]

    @property
    def name(self):
        return self._module_name

    def run(self, project, args, unknown_args):
        raise NotImplementedError("Class %s does not implement a .run() method." % (self.__class__.__name__,))


class Argument(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
