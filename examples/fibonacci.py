def iterative_fibonacci(n):
    a, b = 0, 1

    for i in range(n):
        a, b = b, a + b

    return a


def recursive_fibonacci(n):
    return n if n < 2 else recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Calculate fibonacci numbers")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--iterative",
        action="store_const",
        const=iterative_fibonacci,
        help="Use iterative algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-r",
        "--recursive",
        action="store_const",
        const=recursive_fibonacci,
        help="Use recursive algorithm",
        dest="algorithm",
    )
    parser.set_defaults(algorithm=iterative_fibonacci)

    parser.add_argument("n", type=int, help="The fibonacci number to calculate")

    args = parser.parse_args()

    print(args.algorithm(args.n))
