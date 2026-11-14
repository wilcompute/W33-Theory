"""Exact Lyapunov-Schmidt quartic at the saved F32 regulus stabilizer."""

import json
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from pathlib import Path

import numpy as np

from toe_20261114_regulus_stabilizer_variation import FIXTURE, coset_spectrum, field_tables

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_regulus_q32_quartic.json"


def pauli_coordinates(basis, covered, modes):
    mul, trace = field_tables(5)

    @lru_cache(maxsize=16384)
    def zx(a, b):
        return int(trace[mul[(a >> 10) & 31, b & 31] ^ mul[a >> 15, (b >> 5) & 31]])

    def exponent(a, b):
        # P(a)P(b) = i^exponent(a,b) P(a xor b), P(a) = i^zx(a,a) X(a)Z(a).
        return (zx(a, a) + zx(b, b) - zx(a ^ b, a ^ b) + 2 * zx(a, b)) % 4

    stabilizer = {0: 0}
    for r in basis:
        stabilizer.update({s ^ r: (n + exponent(s, r)) % 4 for s, n in list(stabilizer.items())})
    assert all(n % 2 == 0 for n in stabilizer.values())
    representatives = {r ^ s: r for r in sorted({0} | {r for r, _ in modes}) for s in stabilizer}
    groups = defaultdict(list)
    for v in map(int, covered):
        groups[representatives[v]].append(v)

    def real_element(a, b, v):
        r, p = a
        s, q = b
        phase = (-p + q + exponent(r, v) + exponent(r ^ v, s) - stabilizer[r ^ v ^ s]) % 4
        return (1, 0, -1, 0)[phase]


    # Direct 1024-component control of the multiplication convention.
    sites = np.arange(1024)
    signs = 1 - 2 * trace
    def apply(label, state):
        x = label & 1023
        phase = signs[mul[(label >> 10) & 31, sites & 31] ^ mul[label >> 15, sites >> 5]]
        return (1j**zx(label, label) * phase * state)[sites ^ x]

    state = np.eye(1, 1024, dtype=complex)[0]
    for r in basis:
        state += apply(r, state)
    norm = np.vdot(state, state).real
    assert norm > 0
    assert all(np.array_equal(apply(r, state), state) for r in basis)
    flat = [(0, 0)] + [rp for rp, curvature in modes.items() if curvature == 0]
    for a, b in combinations_with_replacement(flat, 2):
        if not groups[representatives[a[0] ^ b[0]]]:
            continue
        group = groups[representatives[a[0] ^ b[0]]]
        va = 1j**a[1] * apply(a[0], state)
        vb = 1j**b[1] * apply(b[0], state)
        for v in (group[0], group[-1]):
            assert np.vdot(va, apply(v, vb)).real == norm * real_element(a, b, v)
    return representatives, groups, real_element


def accumulate_square(target, pairs, factor):
    for ij, a in pairs.items():
        for lm, b in pairs.items():
            target[tuple(sorted(ij + lm))] += a * b * factor


def reduced_quartic(basis, covered, modes, cost):
    rep, groups, element = pauli_coordinates(basis, covered, modes)
    flat = [rp for rp, curvature in modes.items() if curvature == 0]
    assert not any(rep[a[0] ^ b[0] ^ c[0]] == 0 for a, b, c in combinations(flat, 3))
    reference = (0, 0)
    # For each Pauli v, linear[v] and quadratic[v] encode
    # 2 Re <psi|P_v|u> and <u|P_v|u> on the flat space.
    linear = defaultdict(dict)
    quadratic = defaultdict(dict)
    for i, a in enumerate(flat):
        for v in groups[a[0]]:
            value = 2 * element(reference, a, v)
            if value:
                linear[v][i] = value
        for j in range(i, len(flat)):
            b = flat[j]
            for v in groups[rep[a[0] ^ b[0]]]:
                value = element(a, b, v) * (1 if i == j else 2)
                if value:
                    quadratic[v][i, j] = value

    correction = defaultdict(Counter)
    for v, pairs in quadratic.items():
        r = rep[v]
        if r:
            for p in range(2):
                value = 4 * element(reference, (r, p), v)
                for ij, coefficient in pairs.items():
                    if value:
                        correction[r, p][ij] += value * coefficient
    for v, terms in linear.items():
        for i, coefficient in terms.items():
            for j, a in enumerate(flat):
                r = rep[v ^ a[0]]
                if r:
                    for p in range(2):
                        value = element(a, (r, p), v)
                        if value:
                            correction[r, p][tuple(sorted((i, j)))] += 4 * value * coefficient

    quartic = Counter()
    for pairs in quadratic.values():
        accumulate_square(quartic, pairs, 1)
    accumulate_square(quartic, {(i, i): 1 for i in range(len(flat))}, -cost)
    for rp, pairs in correction.items():
        if modes[rp] == 0:
            assert not any(pairs.values())
        else:
            accumulate_square(quartic, pairs, -Fraction(1, 4 * modes[rp]))

    return flat, {monomial: a for monomial, a in sorted(quartic.items()) if a}, correction


def certify(quartic, count):
    mixed = [((2, 10), (9, 12), Fraction(160)),
             ((2, 12), (9, 10), Fraction(5536, 105)),
             ((5, 6), (11, 12), Fraction(-2048, 55))]
    squares = {tuple(sorted(m)): a for m, a in quartic.items() if m[0] == m[1] and m[2] == m[3]}
    residual = dict(squares)
    cross = Counter()
    for (i, j), (k, l), value in mixed:
        cross[tuple(sorted((i, j, k, l)))] += value
        for a, b in ((i, j), (k, l)):
            residual[a, a, b, b] -= abs(value) / 2
    assert quartic == dict(squares) | dict(cross)
    assert len(squares) == 104 and min(residual.values()) > 0

    # The remaining positive squares force each edge to have a zero endpoint.
    # The allocated mixed squares also vanish on every such support.
    edges = {(i, j) for i, _, j, _ in squares}
    supports = []
    for size in range(count, 0, -1):
        for support in combinations(range(count), size):
            s = set(support)
            if not any(s <= larger for larger in supports) and not any(
                    pair in edges for pair in combinations(support, 2)):
                supports.append(s)
    return mixed, sorted(tuple(sorted(s)) for s in supports), min(residual.values())


def calculate():
    record = json.loads(FIXTURE.read_text(encoding="utf-8"))["q32"]
    hit, covered, modes = coset_spectrum(5, record["basis"])
    assert len(hit) == 11 and min(modes.values()) == 0
    flat, quartic, correction = reduced_quartic(record["basis"], covered, modes, len(hit))
    assert len(flat) == 17
    mixed, supports, margin = certify(quartic, len(flat))
    return dict(status="PASS", flat_coordinates=flat,
                quartic=[[monomial, str(value)] for monomial, value in quartic.items()],
                mixed_square_allocations=[[a, b, str(w)] for a, b, w in mixed],
                smallest_remaining_square_coefficient=str(margin),
                maximal_zero_supports=supports,
                nonzero_second_order_corrections=sum(any(pairs.values()) for pairs in correction.values()))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8")
    print("PASS", len(result["quartic"]), "quartic terms,", len(result["maximal_zero_supports"]),
          "maximal zero supports", flush=True)
