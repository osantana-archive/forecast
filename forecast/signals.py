# coding: utf-8


from blinker import Namespace


signals = Namespace()

start_request = signals.signal("forecast.start_request",
                               doc="Signal emitted by context manager before RequestHandler._execute()")

end_request = signals.signal("forecast.end_request",
                             doc="Signal emitted by context manager after RequestHandler._execute()")

middleware_failure = signals.signal("forecast.middleware_failure",
                                    doc="Signal emitted when a middleware fails.")
