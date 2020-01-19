def simple_bubble_sort(l):
    for j in range(1, len(l))[::-1]:
        for i in range(j):
            if l[i] > l[i + 1]:
                l[i], l[i + 1] = l[i + 1], l[i]


def bubble_sort(l):
    j = len(l) - 1
    while j:
        k = 0
        for i in range(j):
            if l[i] > l[i + 1]:
                l[i], l[i + 1] = l[i + 1], l[i]
                k = i
        j = k


def _merge_sort(l, left, right):
    if right - left > 1:
        middle = (left + right + 1) // 2

        _merge_sort(l, left, middle)
        _merge_sort(l, middle, right)

        r = l[middle:right]
        while r:
            right -= 1

            if l[middle - 1] > r[-1]:
                middle -= 1
                l[right] = l[middle]

                if middle == left:
                    l[left:right] = r
                    break
            else:
                l[right] = r.pop()


def merge_sort(l):
    _merge_sort(l, 0, len(l))


def simple_insertion_sort(l):
    for j in range(1, len(l)):
        for i in range(j)[::-1]:
            if l[i] > l[i + 1]:
                l[i], l[i + 1] = l[i + 1], l[i]


def insertion_sort(l):
    for i in range(1, len(l)):
        x = l[i]
        while i and l[i - 1] > x:
            l[i] = l[i - 1]
            i -= 1
        l[i] = x


def shell_sort(l):
    j = 2 * (len(l) // 4) + 1
    while True:
        for i in range(j, len(l)):
            x = l[i]
            while i >= j and l[i - j] > x:
                l[i] = l[i - j]
                i -= j
            l[i] = x
        if j == 1:
            break
        j = 2 * ((j - 1) // 4) + 1


def selection_sort(l):
    for j in range(1, len(l))[::-1]:
        k = j
        for i in range(j):
            if l[i] > l[k]:
                k = i
        l[j], l[k] = l[k], l[j]


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Sort lists")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-bs",
        "--simple-bubble",
        action="store_const",
        const=simple_bubble_sort,
        help="Use simple bubble sort algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-b",
        "--bubble",
        action="store_const",
        const=bubble_sort,
        help="Use bubble sort algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-m",
        "--merge",
        action="store_const",
        const=merge_sort,
        help="Use merge sort algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-is",
        "--simple-insertion",
        action="store_const",
        const=simple_insertion_sort,
        help="Use simple insertion sort algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-i",
        "--insertion",
        action="store_const",
        const=insertion_sort,
        help="Use insertion sort algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-sh",
        "--shell",
        action="store_const",
        const=shell_sort,
        help="Use shell sort algorithm",
        dest="algorithm",
    )
    group.add_argument(
        "-se",
        "--selection",
        action="store_const",
        const=selection_sort,
        help="Use selection sort algorithm",
        dest="algorithm",
    )
    parser.set_defaults(algorithm=merge_sort)

    parser.add_argument("list", nargs="+", type=int, help="The list of numbers to sort")

    args = parser.parse_args()

    args.algorithm(args.list)
    print(" ".join(map(str, args.list)))
