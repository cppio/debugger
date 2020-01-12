import json
import os.path
import runpy
import sys

from . import *


def main(file, function=None):
    if file.endswith(".py"):
        if function is None:
            scoped_trace(file, runpy.run_path, file, run_name="__main__")
        else:
            module = runpy.run_path(file, run_name=os.path.basename(file)[:-3])

            # Python 2 workaround
            module[function].__globals__.update(module)

            scoped_trace(file, module[function])
    elif file.endswith(".json"):
        if function is not None:
            return "Function cannot be given with output log"

        with open(file) as output:
            output = json.load(output)

        print_output(output)
    else:
        return "Unknown filetype"


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        __package__, description="Traces the execution of a python program"
    )
    parser.add_argument("file", help="The program to execute or the output log to view")
    parser.add_argument(
        "function",
        nargs="?",
        help="The function to trace. This function must able to be called with no arguments. If missing, the program will be called as '__main__' and all function calls will be traced. Not valid if viewing an output log",
    )

    args = parser.parse_args()

    err = main(**vars(args))
    if err:
        print(err)
