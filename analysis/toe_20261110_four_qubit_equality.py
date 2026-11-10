"""Solver-free replay and equality classification for the Pass 12645 dual."""

from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DUAL = ROOT / 'data/toe_20261110_four_qubit_equality.json'


def anticommutes(left, right):
    return ((((left & 15) & (right >> 4)).bit_count()
             + ((left >> 4) & (right & 15)).bit_count()) % 2)


def lagrangians():
    spaces = {(0,)}
    for _ in range(4):
        spaces = {
            tuple(sorted(space + tuple(point ^ member for member in space)))
            for space in spaces
            for point in range(1, 256)
            if point not in space and all(not anticommutes(point, member) for member in space)
        }
    return [set(space[1:]) for space in sorted(spaces)]


def positive_definite(matrix):
    """Sylvester's criterion via fraction-free elimination."""
    a = [row.copy() for row in matrix]
    previous = 1
    for i, row in enumerate(a):
        pivot = row[i]
        if pivot <= 0:
            return False
        for j in range(i + 1, len(a)):
            for k in range(j, len(a)):
                numerator = pivot * a[j][k] - row[j] * row[k]
                a[j][k], remainder = divmod(numerator, previous)
                assert remainder == 0
        previous = pivot
    return True


def verify():
    dual = json.loads(DUAL.read_bytes())
    lines = lagrangians()
    assert len(lines) == 2295
    bases = json.loads((ROOT / 'data/w33_four_qubit_theta_exact.json').read_bytes())['lines']
    covered = set.union(*(lines[i] for i in bases))
    assert len(covered) == 135
    uncovered = sorted(set(range(1, 256)) - covered)
    tight = [line - covered for line in lines if len(line & covered) == 1]
    assert len(tight) == 3 and len(set.union(*tight)) == 42
    for group in tight:
        assert len(group) == 14
        anchor = min(group)
        span = {0}
        for point in group:
            span |= {value ^ anchor ^ point for value in span}
        assert len(span) == 16

    # Build 4 times the dual slack from the signed integer edge multipliers.
    size = len(uncovered)
    edges = [(i, j) for i, j in combinations(range(size), 2)
             if anticommutes(uncovered[i], uncovered[j])]
    weights = dual['edge_multipliers_times_four']
    assert len(weights) == len(edges) == 3360
    slack = [[56 * (i == j) - 4 for j in range(size)] for i in range(size)]
    for (i, j), weight in zip(edges, weights):
        slack[i][j] -= weight
        slack[j][i] -= weight

    groups = [[i for i, point in enumerate(uncovered) if point in group] for group in tight]
    for group in groups:
        assert all(sum(row[i] for i in group) == 0 for row in slack)

    # Multiply the gap test M - (I-P)/5 by 280, where P projects to the
    # disjoint indicator vectors. Remove one coordinate per indicator.
    removed = {group[0] for group in groups}
    group_id = {i: label for label, group in enumerate(groups) for i in group}
    retained = sorted(set(range(size)) - removed)
    gap_matrix = [
        [70 * slack[i][j] - 56 * (i == j) + 4 * (i in group_id and group_id[i] == group_id.get(j))
         for j in retained]
        for i in retained
    ]
    assert positive_definite(gap_matrix)
    result = dict(dual_rank=len(retained), positive_spectral_gap_at_least='1/5',
                  equality_rays=16 * len(tight), uncovered_stabilizer_supports=[sorted(g) for g in tight])
    assert result == dual['verified_result']
    return result


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
