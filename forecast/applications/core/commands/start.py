# coding: utf-8


import os
import shutil
import sys
from forecast.exceptions import CommandError

from forecast.manager import BaseCommand, Argument
from forecast import skels


class StartCommand(BaseCommand):
    help = "Start a project element from skel"
    parameters = (
        Argument("--list-skels", "-l", action="store_true"),
        Argument("--skel", "-s", action="store"),
    )

    def run(self, project, args, unknown_args):
        if not args.list_skels and not args.skel:
            return self.help()

        if args.skel and not unknown_args:
            return self.help()

        if args.list_skels:
            return self.list_skels()

        for dest in unknown_args:
            self.create(args.skel, dest)

    @property
    def skel_path(self):
        return os.path.dirname(os.path.realpath(skels.__file__))

    def _get_skel_list(self):
        return set(os.path.splitext(skel)[0] for skel in os.listdir(self.skel_path) if not skel.startswith("_"))

    def help(self):
        print("Use: %s start --list | --skel=(%s) name1 [name2 [name3]]" % (sys.argv[0], "|".join(self._get_skel_list())))

    def list_skels(self):
        print("Available skels:")
        for skel in sorted(self._get_skel_list()):
            print "   %s" % (skel,)

    def create(self, skel, dest):
        src = os.path.join(self.skel_path, skel)

        if not os.path.exists(src):
            src += ".py"

        if not os.path.exists(src):
            raise CommandError("Skel %s does not exists." % (skel,))

        dest = os.path.realpath(dest)

        if os.path.isdir(src):
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns("*.py[co]"))
        else:
            shutil.copy(src, os.path.join(dest, os.path.basename(src)))
