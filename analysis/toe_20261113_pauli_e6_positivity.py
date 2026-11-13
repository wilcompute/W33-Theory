"""Exact state-positivity tests for the three-qubit Pauli E6 cubic."""

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_pauli_e6_positivity.json"


def pauli(label):
    letters = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.diag([1, -1]).astype(complex),
    }
    result = np.ones((1, 1), dtype=complex)
    for letter in label:
        result = np.kron(result, letters[letter])
    return result


def calculate():
    labels = ["".join(v) for v in product("IXYZ", repeat=3)]
    quaternionic = pauli("YII")
    matrices = {label: pauli(label) for label in labels[1:]}
    even = [label for label, p in matrices.items()
            if np.array_equal(quaternionic @ p.conj(), p @ quaternionic)]
    assert len(even) == 27
    triads = {}
    for a, b, c in combinations(even, 3):
        value = np.trace(matrices[a] @ matrices[b] @ matrices[c])/8
        if value.real:
            assert value in (-1, 1)
            triads[a, b, c] = int(value.real)
    assert len(triads) == 45

    incidence = sp.Matrix([[int(label in triad) for label in even] for triad in triads])
    boosts = incidence.nullspace()
    assert len(boosts) == 6
    line = tuple(sorted(("IZI", "IIZ", "IZZ")))
    assert triads[line] == 1
    h = next(h for h in boosts if any(h[even.index(label)] for label in line))
    denominator = sp.ilcm(*(v.q for v in h))
    weights = [int(v*denominator) for v in h]
    assert incidence * sp.Matrix(weights) == sp.zeros(45, 1)
    if max(weights[even.index(label)] for label in line) <= 0:
        weights = [-w for w in weights]
    boost = dict(zip(even, weights))
    positive = max(line, key=boost.get)
    assert boost[positive] > 0
    initial = {label: 1 for label in line}
    transformed = {label: sp.Integer(2)**boost[label] for label in line}
    assert sp.prod(transformed.values()) == 1

    def density_spectrum(charges):
        x = sum((charges.get(label, 0)*sp.Matrix(matrices[label].real.astype(int).tolist())
                 for label in line), sp.zeros(8))
        return list((sp.eye(8)+x).diagonal()/8)

    initial_density = density_spectrum(initial)
    transformed_density = density_spectrum(transformed)
    assert min(initial_density) == 0 and max(initial_density) == sp.Rational(1, 2)
    assert min(transformed_density) < 0
    assert all(np.trace(matrices[label] @ matrices[label]).real == 8 for label in even)

    # Same quadratic and cubic traces, different positivity. These are
    # duplicated quaternionic spectra of X, in the same diagonal Pauli flat.
    spectra = [[sp.Rational(v, 10) for v in values]
               for values in ((10, -10, 5, -5), (11, -11, 2, -2))]
    moments = [[sum(v**k for v in values) for k in (1, 2, 3, 4)] for values in spectra]
    assert moments[0][:3] == moments[1][:3] and moments[0][3] != moments[1][3]
    assert min(spectra[0]) == -1 and min(spectra[1]) < -1
    return dict(status="PASS", pauli_labels=even, cubic_triads=len(triads),
                diagonal_split_torus_dimension=len(boosts),
                boost_weights=boost, boost_scale=2,
                input_line=line, input_cubic=1, output_cubic=1,
                input_density_spectrum=sorted(map(str, initial_density)),
                output_density_spectrum=sorted(map(str, transformed_density)),
                output_pauli_expectation_above_one=dict(label=positive, value=str(transformed[positive])),
                equal_low_moment_control=dict(spectra=[list(map(str, v)) for v in spectra],
                                              moments_1_to_4=[list(map(str, v)) for v in moments]))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
