# coding: utf-8


import tornado.ioloop

from forecast.manager import BaseCommand, Argument


class RunserverCommand(BaseCommand):
    help_text = "Start a server"
    parameters = (
        Argument("--port", "-p", action="store", default=8888, type=int),
    )

    def run(self, project, args, unknown_args):
        print "Development server is running at http://127.0.0.1:%s/" % (args.port,)
        print "Quit the server with CONTROL-C."

        tornado_application = project.get_tornado_application()
        tornado_application.listen(args.port)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            print "\nInterrupted!"
