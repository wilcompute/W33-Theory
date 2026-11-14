"""Exact common witness for the F8 regulus and its two quotient types."""

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261114_regulus_quotient_witness.json"


def multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return result


def trace(a):
    square = multiply(a, a)
    return a ^ square ^ multiply(square, square)


def determinant(x, z):
    return multiply(x & 7, z & 7) ^ multiply(x >> 3, z >> 3)


def action(state, x, z):
    sites = np.arange(64)
    signs = np.array([1-2*trace(determinant(int(site), z)) for site in sites])
    return (1j**trace(determinant(x, z))*signs*state)[sites ^ x]


def calculate():
    controls = json.loads((ROOT / "data/w33_regulus_f8_and_quotient.json").read_text())
    dual = {sum(trace(multiply(a, b)) << i for i, b in enumerate((1, 2, 4))): a
            for a in range(8)}
    types = {}
    for row in controls["quotients"]:
        p = row["p"]
        x, zz = p & 63, p >> 6
        z = dual[zz & 7] | (dual[zz >> 3] << 3)
        value = determinant(x, z)
        assert trace(value) == 1
        orbit = 1 if value == 1 else 3
        multiplicity = row["top_multiplicities"][2][1]
        assert orbit not in types or types[orbit] == multiplicity
        types[orbit] = multiplicity
    assert sorted(types.values()) == [17, 27]

    saved = np.load(ROOT / "data/w33_f8_minimiser.npy").reshape(-1)
    initial = np.round(saved.real*100000) + 1j*np.round(saved.imag*100000)
    symmetries = [(12, 51), (53, 17), (57, 34)]
    state = initial
    for x, z in symmetries[:2]:
        eigenvalue = int(round(np.vdot(saved, action(saved, x, z)).real))
        assert eigenvalue in (-1, 1)
        state = state + eigenvalue*action(state, x, z)
    eigenvalues = []
    for x, z in symmetries:
        actual = action(state, x, z)
        eigenvalue = 1 if np.array_equal(actual, state) else -1
        assert np.array_equal(actual, eigenvalue*state)
        eigenvalues.append(eigenvalue)

    # Python integers make the expectation-square certificate exact.
    def dot(left, right):
        a = [int(v.real) for v in left]
        b = [int(v.imag) for v in left]
        c = [int(v.real) for v in right]
        d = [int(v.imag) for v in right]
        return sum(u*v + w*y for u,w,v,y in zip(a,b,c,d)), sum(
            u*y-w*v for u,w,v,y in zip(a,b,c,d))

    norm, imag = dot(state, state)
    assert norm > 0 and imag == 0
    covered = [(x,z) for x,z in product(range(64), repeat=2) if (x or z) and not determinant(x,z)]
    assert len(covered) == 567
    value = Fraction(sum(sum(t*t for t in dot(state, action(state, x, z)))
                         for x,z in covered), norm**2)
    assert value < Fraction(249851, 100000)

    witnesses = {}
    for (x, z), eigenvalue in zip(symmetries, eigenvalues):
        det = determinant(x,z)
        if not trace(det):
            continue
        orbit = 1 if det == 1 else 3
        # Replay the quotient objective directly from its commuting
        # Pauli representatives. A covered label has a unique lift.
        reps = set()
        restricted = 0
        for a, b in covered:
            if trace(determinant(a, z) ^ determinant(x, b)):
                assert dot(state, action(state, a, b)) == (0, 0)
                continue
            label = a | (b << 6)
            partner = (a ^ x) | ((b ^ z) << 6)
            coset = min(label, partner)
            assert coset and coset not in reps
            reps.add(coset)
            restricted += sum(t*t for t in dot(state, action(state, a, b)))
        assert len(reps) == 279 and Fraction(restricted, norm**2) == value
        witnesses[types[orbit]] = dict(x=x, z=z, determinant=det, eigenvalue=eigenvalue,
                                      quotient_covered=len(reps))
    assert len(witnesses) == 2
    trace_one = [a for a in range(8) if trace(a) == 1]
    counts = Counter(determinant(x,z) for x,z in product(range(64),repeat=2))
    assert all(counts[d] == 504 for d in trace_one)
    # Any logical stabilizer lifts to the physical stabilizer generated
    # by its commuting representatives and the shortening Pauli.
    fixture = json.loads((ROOT / "data/w33_regulus_stabiliser_minimum.json").read_text())
    span = [0]
    for generator in fixture["q8"]["basis"]:
        span += [v ^ generator for v in span]
    assert len(set(span)) == 64
    assert all(trace(determinant(u & 63, v >> 6) ^ determinant(v & 63, u >> 6)) == 0
               for u, v in product(span, repeat=2))
    assert sum(determinant(v & 63, v >> 6) == 0 for v in span[1:]) == 3
    stabilizer_witnesses = {}
    for v in span:
        det = determinant(v & 63, v >> 6)
        if trace(det):
            stabilizer_witnesses.setdefault(types[1 if det == 1 else 3], v)
    assert set(stabilizer_witnesses) == set(witnesses)
    return dict(status="PASS", trace_one_determinants=trace_one,
                quotient_orbit_sizes=[504, 1512], quotient_witnesses=witnesses,
                stabilizer_shortening_witnesses=stabilizer_witnesses,
                rounded_integer_state=[[int(v.real), int(v.imag)] for v in state],
                exact_common_upper=str(value), decimal_common_upper=float(value))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result["quotient_witnesses"], result["exact_common_upper"], result["decimal_common_upper"])
