import collections


def binary_search(l, x):
    left, right = 0, len(l)

    while left < right:
        middle = (left + right) // 2

        if l[middle] < x:
            left = middle + 1
        elif l[middle] > x:
            right = middle
        else:
            return middle

    raise ValueError("{!r} is not in list".format(x))


def depth_first_search(neighbors, vertex):
    visited = set()
    to_visit = [vertex]

    while to_visit:
        vertex = to_visit.pop()

        if vertex not in visited:
            yield vertex

            visited.add(vertex)
            to_visit.extend(
                neighbor
                for neighbor in reversed(neighbors[vertex])
                if neighbor not in visited
            )


def breadth_first_search(neighbors, vertex):
    visited = {vertex}
    to_visit = collections.deque([vertex])

    while to_visit:
        vertex = to_visit.popleft()
        yield vertex

        for neighbor in neighbors[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                to_visit.append(neighbor)


_binary_search = binary_search
_depth_first_search = depth_first_search
_breadth_first_search = breadth_first_search


def binary_search(seq=range(0, 1024, 4), x=340):
    return _binary_search(seq, x)


neighbors = {
    "A": "BCE",
    "B": "ADF",
    "C": "AG",
    "D": "B",
    "E": "AF",
    "F": "BE",
    "G": "C",
}


def depth_first_search(neighbors=neighbors, x="A"):
    return list(_depth_first_search(neighbors, x))


def breadth_first_search(neighbors=neighbors, x="A"):
    return list(_breadth_first_search(neighbors, x))
