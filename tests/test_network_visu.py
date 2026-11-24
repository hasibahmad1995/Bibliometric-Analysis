import numpy as np

from utils.visualization.network_visu import create_keyword_network, nor


def test_nor_maps_min_to_5_and_max_to_50():
    assert nor(1, 1, 11) == 5
    assert nor(11, 1, 11) == 50
    assert nor(6, 1, 11) == 27.5


def test_nor_uses_middle_size_when_all_counts_are_equal():
    assert nor(4, 4, 4) == 27.5


def test_edges_only_for_pairs_that_appear_together():
    keywords = ["a", "b", "c"]
    info = {k: {"keyword": k, "count": n} for k, n in zip(keywords, [3, 2, 1])}
    matrix = np.array([
        [0, 2, 0],
        [2, 0, 1],
        [0, 1, 0],
    ])

    nodes, edges = create_keyword_network(keywords, info, matrix)

    assert [n["name"] for n in nodes] == ["a", "b", "c"]
    assert nodes[0]["symbolSize"] == 50  # most frequent keyword is largest
    assert nodes[2]["symbolSize"] == 5   # least frequent keyword is smallest
    assert edges == [
        {"source": "a", "target": "b", "value": 2},
        {"source": "b", "target": "c", "value": 1},
    ]
