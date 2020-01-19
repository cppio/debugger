import json
import os.path
import runpy
import sys

from . import scoped_trace, print_output


def trace(
    file, arguments=(), function=None, output=False, save=None, local=False, eval=False
):
    if function is None:
        sys.argv = [file] + list(arguments)
        scoped_trace(file, runpy.run_path, file, run_name="__main__")
    else:
        module = runpy.run_path(file, run_name=os.path.basename(file)[:-3])

        # Python 2 workaround
        module[function].__globals__.update(module)

        scoped_trace(file, module[function], *arguments)


def view(file, timing=False, report=True):
    with open(file) as output:
        output = json.load(output)

    print_output(output, timing=timing, report=report)


if __name__ == "__main__":
    from argparse import ArgumentParser, REMAINDER

    parser = ArgumentParser(
        __package__, description="Traces the execution of a python program"
    )
    subparsers = parser.add_subparsers()

    trace_parser = subparsers.add_parser("trace")
    trace_parser.set_defaults(subcommand=trace)
    trace_parser.add_argument("file", help="The program to execute")
    trace_parser.add_argument(
        "-f",
        "--function",
        help="The function to trace. This function must able to be called with no arguments or only string arguments. If unspecified, the program will be called as '__main__' and all function calls will be traced.",
        metavar="func",
    )
    trace_parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="Prints trace immediately instead of saving to file",
    )
    trace_parser.add_argument(
        "-s",
        "--save",
        help="Saves trace to file instead of the default <file>.json. Can be used with -o",
        metavar="trace",
    )
    trace_parser.add_argument(
        "-l", "--local", action="store_true", help="Do not trace outside functions"
    )
    trace_parser.add_argument(
        "-e",
        "--eval",
        action="store_true",
        help="Evaluates the arguments. Only valid with -f",
    )
    trace_parser.add_argument(
        "arguments",
        nargs=REMAINDER,
        help="The arguments to pass to the program. If -f is set, then these will be passed as position str arguments.",
    )

    view_parser = subparsers.add_parser("view")
    view_parser.set_defaults(subcommand=view)
    view_parser.add_argument("file", help="The output log to view")
    view_parser.add_argument(
        "-t", "--timing", action="store_true", help="Show timing information"
    )
    view_parser.add_argument(
        "-n",
        "--no-report",
        action="store_false",
        help="Hide the final variable information",
        dest="report",
    )

    args = parser.parse_args()
    subcommand = vars(args).pop("subcommand", None)

    if subcommand is None:
        parser.error("too few arguments")

    subcommand(**vars(args))
