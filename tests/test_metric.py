import asyncio
from itertools import combinations

import pytest

from use_case.use_case import metric

# First example graph from `generator`: 6 edges of weight 1.
GRAPH = [
    (0, 1, 1.0),
    (0, 2, 1.0),
    (0, 4, 1.0),
    (1, 2, 1.0),
    (2, 3, 1.0),
    (3, 4, 1.0),
]


def run(solution, graph=GRAPH):
    return asyncio.run(metric(solution, graph))


@pytest.mark.parametrize(
    "s, t, expected",
    [
        ([0, 3], [1, 2, 4], 5 / 6),
        ([0, 2, 3], [1, 4], 4 / 6),
        ([0], [1, 2, 3, 4], 3 / 6),
        ([3], [0, 1, 2, 4], 2 / 6),
    ],
)
def test_metric_is_cut_weight_over_total(s, t, expected):
    assert run((s, t)) == pytest.approx(expected)
    # The cut is symmetric in s and t.
    assert run((t, s)) == pytest.approx(expected)


def test_metric_uses_edge_weights():
    graph = [(0, 1, 2.0), (1, 2, 3.0), (0, 2, 5.0)]
    assert run(([0], [1, 2]), graph) == pytest.approx(7 / 10)
    assert run(([2], [0, 1]), graph) == pytest.approx(8 / 10)


def test_metric_matches_brute_force_on_all_partitions():
    nodes = range(5)
    for size in range(1, 5):
        for s in combinations(nodes, size):
            t = [n for n in nodes if n not in s]
            cut = sum(
                w for a, b, w in GRAPH if (a in s) != (b in s)
            )
            assert run((list(s), t)) == pytest.approx(cut / 6)


def test_metric_empty_graph():
    assert run(([0], [1]), []) == 0.0
