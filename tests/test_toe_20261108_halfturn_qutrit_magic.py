"""Replay the exact qutrit phase-space witness from the half-turn certificate."""

from collections import Counter
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_compressed_matter_parity_wigner_negativity():
    path = ROOT / 'data/toe_20261108_native_spin_halfturn.json'
    certificate = json.loads(path.read_text(encoding='utf-8'))
    by_column = {j: (i, int(value)) for i, j, value in certificate['forced_family_species_operator']}
    signs = {}
    for j, (i, first) in by_column.items():
        k, second = by_column[i]
        assert k == j
        signs[divmod(j, 3)] = first * second
    assert signs == {(a, b): (-1 if a and b else 1) for a, b in product(range(3), repeat=2)}

    # Uniform input gives amplitudes sign/3. In F3 the inverse of two is two.
    # Wigner coefficients then have denominator 9 * 3**2 = 81.
    points = list(product(range(3), repeat=2))
    histogram = Counter()
    for (a, b), (p, q) in product(points, repeat=2):
        phase_totals = [0, 0, 0]
        for x, y in points:
            left = signs[(a+2*x) % 3, (b+2*y) % 3]
            right = signs[(a-2*x) % 3, (b-2*y) % 3]
            phase_totals[(-p*x-q*y) % 3] += left * right
        assert phase_totals[1] == phase_totals[2]
        histogram[phase_totals[0] - phase_totals[1]] += 1

    assert histogram == {0: 32, 1: 4, 4: 16, 6: 8, 9: 1, -2: 16, -3: 4}
    assert sum(v*n for v, n in histogram.items()) == 81
    assert sum(abs(v)*n for v, n in histogram.items()) == 169
