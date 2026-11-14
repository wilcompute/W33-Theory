"""Exact parity and local variation tests for binary regulus stabilizers."""

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from toe_20261114_regulus_quotient_witness import action, multiply, trace

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data/w33_regulus_odd_k_structure.json"
OUT = ROOT / "data/toe_20261114_regulus_stabilizer_variation.json"


def field_tables(k):
    q = 1 << k
    if k == 3:
        return (np.array([[multiply(a, b) for b in range(q)] for a in range(q)]),
                np.array([trace(a) for a in range(q)]))

    def mul(a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & q:
                a ^= 0b100101
        return result

    table = np.array([[mul(a, b) for b in range(q)] for a in range(q)])
    traces = []
    for a in range(q):
        total = 0
        for _ in range(k):
            total ^= a
            a = table[a, a]
        assert total in (0, 1)
        traces.append(total)
    return table, np.array(traces)


def coset_spectrum(k, basis):
    q = 1 << k
    d = q * q
    mul, trace = field_tables(k)

    def parts(labels):
        return [(labels >> shift) & (q - 1) for shift in range(0, 4 * k, k)]

    def pairing(a, b):
        x, y, z, w = parts(a)
        u, v, s, t = parts(b)
        return trace[mul[x, s] ^ mul[y, t] ^ mul[z, u] ^ mul[w, v]]

    x, y, z, w = parts(np.arange(d*d))
    singular = (mul[x, z] ^ mul[y, w]) == 0
    subgroup = np.array([0])
    for b in basis:
        assert not np.any(pairing(b, subgroup))
        subgroup = np.r_[subgroup, subgroup ^ b]
    assert len(set(subgroup)) == d
    covered = np.flatnonzero(singular)[1:]
    hit = subgroup[singular[subgroup] & (subgroup != 0)]
    seen = np.zeros(d*d, dtype=bool)
    seen[subgroup] = True
    modes = {}
    for r in range(1, d*d):
        if seen[r]:
            continue
        coset = r ^ subgroup
        seen[coset] = True
        coset_hits = coset[singular[coset]]
        off = int(pairing(r, hit).sum())
        odd = int(pairing(r, coset_hits).sum())
        even = len(coset_hits) - odd
        assert len(coset_hits) % 2 == 0
        # Coefficient of the squared real or imaginary tangent coordinate.
        modes[r, 0] = 4 * (even - off)
        modes[r, 1] = 4 * (odd - off)
    assert len(modes) == 2 * (d - 1)
    return hit, covered, modes


def exact_descent(basis, covered, modes):
    state = np.eye(64, dtype=complex)[0]
    for b in basis:
        image = action(state, b & 63, b >> 6)
        state = state + image if np.any(state + image) else state - image

    def tangent(r, phase):
        return 1j**phase * action(state, r & 63, r >> 6)

    first = [(257, 1, -1), (268, 1, -1), (274, 0, -1), (287, 0, 1)]
    second = [(13, 0, -4), (19, 0, 4), (30, 0, -1)]
    assert all(modes[r, p] == 0 for r, p, _ in first)
    assert all(modes[r, p] > 0 for r, p, _ in second)
    polynomials = np.array([2 * state, sum(c*tangent(r, p) for r, p, c in first)*2,
                            sum(c*tangent(r, p) for r, p, c in second)])
    # For these Gaussian integers the absolute product and dot-sum bounds
    # ensure exact arithmetic in binary64 before conversion to Python ints.
    assert 256 * int(np.max(np.abs(polynomials)) + 1)**2 < 2**53

    def moments(vectors):
        coefficients = [0] * 5
        for i, row in enumerate(polynomials):
            for j, vector in enumerate(vectors):
                term = np.vdot(row, vector)
                coefficients[i+j] += int(term.real)
        return coefficients

    norm = moments(polynomials)

    def square(coefficients):
        return [sum(coefficients[i]*coefficients[j] for i in range(5)
                    for j in range(5) if i+j == degree) for degree in range(9)]

    denominator = square(norm)
    difference = [-3*c for c in denominator]
    for label in covered:
        x, z = int(label) & 63, int(label) >> 6
        coefficients = moments([action(v, x, z) for v in polynomials])
        difference = [a+b for a, b in zip(difference, square(coefficients))]
    assert difference[:4] == [0]*4
    assert Fraction(difference[4], denominator[0]) == -40
    t = Fraction(1, 4)
    value = 3 + sum(c*t**i for i, c in enumerate(difference)) / sum(
        c*t**i for i, c in enumerate(denominator))
    assert value < 3
    common = denominator[0]
    assert all(c % common == 0 for c in difference)
    return dict(first_order=first, twice_second_order=second,
                objective_difference_numerator=[c//common for c in difference],
                exact_value_at_one_quarter=str(value))


def calculate():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = {}
    for k, cost, zeros in [(3, 3, 32), (5, 11, 17)]:
        key = f"q{1 << k}"
        basis = fixture[key]["basis"]
        hit, covered, modes = coset_spectrum(k, basis)
        spectrum = Counter(modes.values())
        assert len(hit) == cost and min(spectrum) == 0 and spectrum[0] == zeros
        result[key] = dict(cost=cost, quadratic_coefficients=dict(sorted(spectrum.items())))
        if k == 3:
            result[key]["exact_descent"] = exact_descent(basis, covered, modes)
    return result


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
