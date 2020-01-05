__all__ = ["trace_with"]

import sys


def trace_with(trace, func, *args, **kwds):
    old_trace = sys.gettrace()
    try:
        sys.settrace(trace)
        return func(*args, **kwds)
    finally:
        sys.settrace(old_trace)
