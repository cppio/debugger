from numbers import Real

__all__ = ["log_range"]


def join(sequence):
    items = [j for i in sequence for j in (i, ", ")]
    items.pop()

    if len(items) > 1:
        items[-2] = " and "

    return "".join(items)


def log_range(callback, name, values, function):
    types = join({type(value).__name__ for lineno, value in values})

    if all(isinstance(value, Real) for lineno, value in values):
        least = min(value for lineno, value in values)
        most = max(value for lineno, value in values)
        callback(
            "{}: {} between {} and {} in {}".format(name, types, least, most, function)
        )
    else:
        callback("{}: {} in {}".format(name, types, function))
