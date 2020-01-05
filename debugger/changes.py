__all__ = ["log_changes"]

try:
    from collections.abc import Mapping, Sequence, Set
    from itertools import zip_longest
except ImportError:
    from collections import Mapping, Sequence, Set
    from itertools import izip_longest as zip_longest


def log_changes(callback, name, old_value, value, sentinel=None):
    if old_value is not value and old_value != value:
        if old_value is sentinel:
            callback("{} set to {!r}".format(name, value))
        elif value is sentinel:
            callback("{} removed (was {!r})".format(name, old_value))
        else:
            sentinel = object()

            if isinstance(old_value, Sequence) and isinstance(value, Sequence):
                for n, (i, j) in enumerate(
                    zip_longest(old_value, value, fillvalue=sentinel)
                ):
                    log_changes(callback, "{}[{!r}]".format(name, n), i, j, sentinel)
            elif isinstance(old_value, Mapping) and isinstance(value, Mapping):
                for i in set(old_value) | set(value):
                    log_changes(
                        callback,
                        "{}[{!r}]".format(name, i),
                        old_value.get(i, sentinel),
                        value.get(i, sentinel),
                        sentinel,
                    )
            elif isinstance(old_value, Set) and isinstance(value, Set):
                added = {i for i in value if i not in old_value}
                if added:
                    callback("{} added {}".format(name, added))

                removed = {i for i in old_value if i not in value}
                if removed:
                    callback("{} removed {}".format(name, removed))
            else:
                callback("{} changed from {!r} to {!r}".format(name, old_value, value))
