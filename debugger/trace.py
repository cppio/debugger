__all__ = ["Trace", "trace"]

import copy
import json

try:
    from time import perf_counter
except ImportError:
    from time import clock as perf_counter

from .output import print_output
from .util import trace_with, val_diffs, val_range


def deepcopy(value):
    try:
        return copy.deepcopy(value)
    except Exception:
        return value


class Trace(object):
    def __init__(self, filename=None):
        self.filename = filename
        self.frames = {}
        self.values = {}
        self.lines = {}
        self.begin = perf_counter()
        self.variables = {}
        self.steps = []

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

            diffs = []
            step = {
                "type": event,
                "now": now,
                "lineno": lineno,
                "count": count,
                "total": total,
                "diffs": diffs,
            }
            self.steps.append(step)

            sentinel = object()

            for name, value in frame.f_locals.items():
                old_value = locals.get(name, sentinel)

                diffs.extend(val_diffs(name, old_value, value, sentinel))

                if old_value is not value and old_value != value:
                    self.values[frame].setdefault(name, []).append(
                        (lineno, deepcopy(value))
                    )

            if event == "return":
                vars = self.variables.setdefault(frame.f_code.co_name, {})

                frame_values = step["frame_values"] = []
                step["code_name"] = frame.f_code.co_name

                for name, values in self.values[frame].items():
                    frame_values.append(
                        {
                            "name": name,
                            "range": val_range(value for lineno, value in values),
                            "values": [
                                (lineno, repr(value)) for lineno, value in values
                            ],
                        }
                    )
                    vars.setdefault(name, []).extend(values)

                del self.frames[frame]
                del self.values[frame]

    def report(self):
        now = perf_counter()

        output = {"steps": self.steps, "running_time": now - self.begin}

        lines = output["lines"] = []

        lines.extend(
            {"lineno": lineno, "count": count}
            for lineno, (count, total) in sorted(self.lines.items())
        )

        vars = output["vars"] = []

        for function, variables in self.variables.items():
            for name, values in variables.items():
                vars.append(
                    {
                        "name": name,
                        "range": val_range(value for lineno, value in values),
                        "function": function,
                        "initial": repr(values[0][1]),
                        "final": repr(values[-1][1]),
                    }
                )

        if self.filename is None:
            print_output(output)
        else:
            with open(self.filename + ".json", "w") as file:
                json.dump(output, file)


def trace(func, *args, **kwds):
    trace = Trace()
    ret = trace_with(trace, func, *args, **kwds)
    trace.report()
    return ret
