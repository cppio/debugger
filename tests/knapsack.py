def unbounded_knapsack(vs, ws, W):
    ms = [0]

    for w in range(1, W + 1):
        ms.append(
            max([vi + ms[w - wi] for vi, wi in zip(vs, ws) if wi <= w] or [0])
        )

    return ms[W]


def knapsack(vs, ws, W):
    ms = [[0] * (W + 1)]

    for w, v, m in zip(ws, vs, ms):
        mi = []
        ms.append(mi)

        for j in range(W + 1):
            if w > j:
                mi.append(m[j])
            else:
                mi.append(max(m[j], m[j - w] + v))

    return ms[-1][W]


_knapsack = knapsack
_unbounded_knapsack = unbounded_knapsack


def knapsack(vs=(4, 2, 10, 1, 2), ws=(12, 1, 4, 1, 2), W=15):
    return _knapsack(vs, ws, W)


def unbounded_knapsack(vs=(4, 2, 10, 1, 2), ws=(12, 1, 4, 1, 2), W=15):
    return _unbounded_knapsack(vs, ws, W)
