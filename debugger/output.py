__all__ = ["print_output"]


def diff_to_str(diff):
    if diff["type"] == "set":
        message = "set to {to}"
    elif diff["type"] == "del":
        message = "was removed (was {from})"
    elif diff["type"] == "add":
        return "{} added {{{}}}".format(diff["name"], ", ".join(diff["added"]))
    elif diff["type"] == "remove":
        return "{} removed {{{}}}".format(diff["name"], ", ".join(diff["removed"]))
    elif diff["type"] == "change":
        message = "changed from {from} to {to}"

    return " ".join((diff["name"], message.format(**diff)))


def join(sequence):
    items = [j for i in sequence for j in (i, ", ")]
    items.pop()

    if len(items) > 2:
        items[-2] = " and "

    return "".join(items)


def range_to_str(range):
    types = join(range["types"])

    if range["type"] == "real":
        return "{} between {min} and {max}".format(types, **range)

    return types


def print_step(step):
    lineno, count, total = step["lineno"], step["count"], step["total"]

    print("executed line {} {} time{}".format(lineno, count, "s" if count > 1 else ""))
    print("  total: {} secs".format(total))
    print("  avg: {} secs".format(total / count))

    for diff in step["diffs"]:
        print("line {}: {}".format(lineno, diff_to_str(diff)))

    if step["type"] == "return":
        code_name = step["code_name"]

        for frame_value in step["frame_values"]:
            print(
                "{}: {} in {}".format(
                    frame_value["name"], range_to_str(frame_value["range"]), code_name
                )
            )

            for lineno, value in frame_value["values"]:
                print("  set to {} on line {}".format(value, lineno))


def print_output(output):
    for step in output["steps"]:
        print_step(step)

    print("total running time: {}".format(output["running_time"]))

    for line in output["lines"]:
        print(
            "line {} was run {} time{}".format(
                line["lineno"], line["count"], "s" if line["count"] > 1 else ""
            )
        )

    for var in output["vars"]:
        print(
            "{}: {} in {}".format(
                var["name"], range_to_str(var["range"]), var["function"],
            )
        )
        print("  initial value: {}".format(var["initial"]))
        print("  final value: {}".format(var["final"]))
