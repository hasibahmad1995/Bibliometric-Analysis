import numpy as np

from utils.social_network import build_network_data, split_items

PAPERS = [
    "machine learning; deep learning; healthcare",
    "machine learning; deep learning",
    "machine learning; healthcare",
]


def test_split_items_strips_spaces_and_drops_empty_items():
    assert split_items(" a ; b;;c ;") == ["a", "b", "c"]


def test_split_items_returns_empty_list_for_missing_cell():
    assert split_items(np.nan) == []
    assert split_items(None) == []


def test_items_are_counted_and_sorted_most_frequent_first():
    items, info, _ = build_network_data(PAPERS, top_n=3)

    assert items[0] == "machine learning"
    assert info["machine learning"]["count"] == 3
    assert info["deep learning"]["count"] == 2
    assert info["healthcare"]["count"] == 2


def test_pairs_are_counted_once_per_paper():
    items, _, matrix = build_network_data(PAPERS, top_n=3)
    ml = items.index("machine learning")
    dl = items.index("deep learning")
    hc = items.index("healthcare")

    assert matrix[ml, dl] == 2
    assert matrix[ml, hc] == 2
    assert matrix[dl, hc] == 1


def test_matrix_is_symmetric_with_zero_diagonal():
    _, _, matrix = build_network_data(PAPERS, top_n=3)

    assert (matrix == matrix.T).all()
    assert (np.diag(matrix) == 0).all()


def test_only_top_n_items_are_kept():
    items, info, matrix = build_network_data(PAPERS, top_n=2)

    assert len(items) == 2
    assert set(info) == set(items)
    assert matrix.shape == (2, 2)


def test_repeated_item_in_one_paper_counts_one_pair():
    items, _, matrix = build_network_data(["a; b; a"], top_n=2)

    assert matrix[items.index("a"), items.index("b")] == 1
