from collections import Counter
from itertools import combinations

import numpy as np
import pandas as pd


def split_items(cell):
    """Split a ';'-separated Scopus cell into stripped, non-empty items."""
    if pd.isna(cell):
        return []
    return [item.strip() for item in str(cell).split(';') if item.strip()]


def build_network_data(series, top_n):
    """Count the items in a ';'-separated column and build a co-occurrence matrix for the top_n.

    Only the top_n most frequent items get a row and column, so the matrix is
    top_n x top_n however many distinct items the column holds.

    Returns (items, info, matrix):
      items  - list of the top_n item names, most frequent first
      info   - {item: {'keyword': item, 'count': occurrences}}
      matrix - symmetric int array, matrix[i, j] = papers listing items i and j together
    """
    rows = [split_items(cell) for cell in series]
    counts = Counter(item for row in rows for item in row)

    top = counts.most_common(top_n)
    items = [name for name, _ in top]
    index = {name: i for i, name in enumerate(items)}
    info = {name: {'keyword': name, 'count': count} for name, count in top}

    matrix = np.zeros((len(items), len(items)), dtype=int)
    for row in rows:
        present = sorted({index[item] for item in row if item in index})
        for i, j in combinations(present, 2):
            matrix[i, j] += 1
            matrix[j, i] += 1

    return items, info, matrix
