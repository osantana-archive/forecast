# coding: utf-8


from collections import OrderedDict
from forecast.exceptions import CommandError

from forecast.manager import BaseCommand, Argument


class ShellCommand(BaseCommand):
    help = "Start a interactive Python shell"
    parameters = (
        Argument("--shell", action="store", default=None),
    )

    def run(self, project, args, unknown_args):
        shells = OrderedDict((
            ('bpython', self.bpython),
            ('ipython', self.ipython),
            ('python', self.python),
        ))

        if args.shell:
            try:
                return shells[args.shell](project, args, unknown_args)
            except KeyError:
                raise CommandError("Shell %s is not available." % (args.shell,))

        for shell in shells.values():
            try:
                return shell(project, args, unknown_args)
            except ImportError:
                continue

        raise CommandError("No python shell available! Why not? I have no fucking idea! :D")

    def python(self, project, args, unknown_args):
        import code
        code.interact(local={'project': project})

    def ipython(self, project, args, unknown_args):
        from IPython.frontend.terminal.ipapp import TerminalIPythonApp
        app = TerminalIPythonApp.instance()
        app.initialize(argv=[])
        app.start()

    def bpython(self, project, args, unknown_args):
        import bpython
        bpython.embed()
