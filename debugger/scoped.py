__all__ = ["ScopedTrace", "scoped_trace"]

from .trace import Trace
from .util import trace_with


class ScopedTrace(Trace):
    def __init__(self, scope, *args, **kwargs):
        super(ScopedTrace, self).__init__(*args, **kwargs)
        self.scope = scope

    def __call__(self, frame, event, arg):
        if (
            frame.f_code.co_filename == self.scope
            and frame.f_code.co_name != "<module>"
        ):
            return super(ScopedTrace, self).__call__(frame, event, arg)

        return self


def scoped_trace(scope, func, *args, **kwds):
    scoped_trace = ScopedTrace(scope, scope)
    ret = trace_with(scoped_trace, func, *args, **kwds)
    scoped_trace.report()
    return ret
