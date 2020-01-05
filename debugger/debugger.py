from __future__ import print_function

from copy import deepcopy
import sys

try:
    from time import perf_counter
except ImportError:
    from time import clock as perf_counter

from .changes import log_changes
from .range import log_range

__all__ = ["Trace", "trace"]


class Trace:
    def __init__(self):
        self.frames = {}
        self.values = {}
        self.lines = {}
        self.begin = perf_counter()
        self.variables = {}

    def store_frame(self, frame):
        now = perf_counter()
        self.frames[frame] = frame.f_lineno, deepcopy(frame.f_locals), now
        return now

    def __call__(self, frame, event, arg):
        if event == "call":
            self.store_frame(frame)
            self.values[frame] = {
                name: [(frame.f_lineno, deepcopy(value))]
                for name, value in frame.f_locals.items()
            }

            return self
        elif event in {"line", "return"}:
            lineno, locals, before = self.frames[frame]
            now = self.store_frame(frame)

            count, total = self.lines.get(lineno, (0, 0))
            count += 1
            total += now - before
            self.lines[lineno] = count, total

            print(
                "executed line {} {} time{}".format(
                    lineno, count, "s" if count > 1 else ""
                )
            )
            print("  total: {} secs".format(total))
            print("  avg: {} secs".format(total / count))

            sentinel = object()

            for name, value in frame.f_locals.items():
                old_value = locals.get(name, sentinel)

                log_changes(
                    lambda message: print("line {}:".format(lineno), message),
                    name,
                    old_value,
                    value,
                    sentinel,
                )

                if old_value is not value and old_value != value:
                    self.values[frame].setdefault(name, []).append(
                        (lineno, deepcopy(value))
                    )

            if event == "return":
                vars = self.variables.setdefault(frame.f_code.co_name, {})

                for name, values in self.values[frame].items():
                    log_range(print, name, values, frame.f_code.co_name)

                    for lineno, value in values:
                        print("  set to {!r} on line {}".format(value, lineno))

                    vars.setdefault(name, []).extend(values)

                del self.frames[frame]
                del self.values[frame]

    def report(self):
        now = perf_counter()

        print("total running time: {}".format(now - self.begin))

        for lineno, (count, total) in sorted(self.lines.items()):
            print(
                "line {} was run {} time{}".format(
                    lineno, count, "s" if count > 1 else ""
                )
            )

        for function, variables in self.variables.items():
            for name, values in variables.items():
                log_range(print, name, values, function)
                print("  initial value: {!r}".format(values[0][1]))
                print("  final value: {!r}".format(values[-1][1]))


def trace(func, *args, **kwds):
    old_trace = sys.gettrace()
    trace = Trace()
    try:
        sys.settrace(trace)
        return func(*args, **kwds)
    finally:
        sys.settrace(old_trace)
        trace.report()
