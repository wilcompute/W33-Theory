"""Verify a split E6 torus that attains the Pauli charge norm minimum."""

import json
from pathlib import Path

import numpy as np
import sympy as sp

from toe_20261114_exact_gaussian_us8_pauli_clock import OUT as DICTIONARY, P, R

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_e6_attractor_torus.json"


def calculate():
    _, cubic, _, _, _ = R.load()
    fixture = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    labels = {int(i): v for i, v in fixture["coordinate_to_pauli_label"].items()}
    sign = {i: -1 if i in fixture["coordinate_negative_sign_indices"] else 1 for i in labels}
    diagonal_labels = (16, 32, 48)
    triad = tuple(next(i for i, label in labels.items() if label == v) for v in diagonal_labels)
    assert cubic[tuple(sorted(triad))] * np.prod([sign[i] for i in triad]) == 1

    incidence = sp.Matrix([[int(i in term) for i in range(27)] for term in sorted(cubic)])
    torus = incidence.col_join(sp.eye(27)[list(triad), :])
    weights = []
    for target in [(1, 0, -1), (0, 1, -1)]:
        witness, free = torus.gauss_jordan_solve(sp.Matrix([0]*len(cubic) + list(target)))
        witness = witness.subs(dict.fromkeys(free, 0))
        assert all(x.is_Integer for x in witness)
        assert incidence * witness == sp.zeros(len(cubic), 1)
        assert tuple(witness[list(triad), :]) == target
        weights.append(list(map(int, witness)))

    # Four quaternionic eigenvalues, from the simultaneous sign characters.
    chars = sorted(set(zip(*(map(int, np.diag(P(v)).real) for v in diagonal_labels), strict=True)))
    assert chars == [(-1, -1, 1), (-1, 1, -1), (1, -1, -1), (1, 1, 1)]
    a, b, c = sp.symbols("a b c", real=True)
    values = [i*a + j*b + k*c for i, j, k in chars]
    assert sp.expand(sum(x**3 for x in values)/24) == a*b*c
    assert sp.expand(sum(x**2 for x in values)/4) == a*a+b*b+c*c

    for charge, target in [((1, 8, 27), (6, 6, 6)), ((-1, 8, 27), (-6, 6, 6)),
                           ((1, -8, -27), (6, -6, -6))]:
        product = int(np.prod(charge))
        assert int(np.prod(target)) == product
        assert sum(x*x for x in target)**3 == 27*product**2
        signs = tuple(np.sign(charge))
        chosen = tuple(np.sign(product)*v for v in signs)
        initial = [sum(s*v for s, v in zip(row, charge, strict=True)) for row in chars]
        assert chars[initial.index(max(initial) if product > 0 else min(initial))] == chosen

    # For each pattern of zero components, assign negative weights on all
    # occupied coordinates and balance them on a zero coordinate.
    contractions = []
    for mask in range(1, 7):
        active = [i for i in range(3) if mask & (1 << i)]
        rate = [-int(i in active) for i in range(3)]
        rate[rate.index(0)] = len(active)
        full_rate = rate[0]*np.array(weights[0]) + rate[1]*np.array(weights[1])
        assert list(full_rate[list(triad)]) == rate
        contractions.append(dict(active=active, rates=rate))
    return dict(status="PASS", native_coordinates=triad, pauli_labels=diagonal_labels,
                torus_weights=weights, characters=chars, zero_cubic_contractions=contractions)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
