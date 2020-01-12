__all__ = ["trace_with", "val_diffs", "val_range"]

from numbers import Real
import sys

try:
    from collections.abc import Mapping, Sequence, Set
    from itertools import zip_longest
except ImportError:
    from collections import Mapping, Sequence, Set
    from itertools import izip_longest as zip_longest


def trace_with(trace, func, *args, **kwds):
    old_trace = sys.gettrace()
    try:
        sys.settrace(trace)
        return func(*args, **kwds)
    finally:
        sys.settrace(old_trace)


def val_diffs(name, old_value, value, sentinel=None):
    if old_value is value or old_value == value:
        return []

    if old_value is sentinel:
        return [{"type": "set", "name": name, "to": repr(value)}]

    if value is sentinel:
        return [{"type": "del", "name": name, "from": repr(old_value)}]

    sentinel = object()

    if isinstance(old_value, Sequence) and isinstance(value, Sequence):
        diffs = []

        for n, (i, j) in enumerate(zip_longest(old_value, value, fillvalue=sentinel)):
            diffs.extend(val_diffs("{}[{!r}]".format(name, n), i, j, sentinel))

        return diffs

    if isinstance(old_value, Mapping) and isinstance(value, Mapping):
        diffs = []

        for i in set(old_value) | set(value):
            diffs.extend(
                val_diffs(
                    "{}[{!r}]".format(name, i),
                    old_value.get(i, sentinel),
                    value.get(i, sentinel),
                    sentinel,
                )
            )

        return diffs

    if isinstance(old_value, Set) and isinstance(value, Set):
        diffs = []

        added = {i for i in value if i not in old_value}
        if added:
            diffs.append({"type": "add", "name": name, "added": list(map(repr, added))})

        removed = {i for i in old_value if i not in value}
        if removed:
            diffs.append(
                {"type": "remove", "name": name, "removed": list(map(repr, removed))}
            )

        return diffs

    return [
        {"type": "change", "name": name, "from": repr(old_value), "to": repr(value)}
    ]


def val_range(values):
    values = tuple(values)

    types = sorted({type(value).__name__ for value in values})

    if all(isinstance(value, Real) for value in values):
        return {
            "type": "real",
            "types": types,
            "min": str(min(values)),
            "max": str(max(values)),
        }
    else:
        return {"type": "other", "types": types}
