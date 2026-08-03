#!/usr/bin/env python3
"""Pass 2918: exact first-order census for every closed two-copy M36 stabilizer branch.

Pass 2861 proves that no branch in the full [[4,2]] stabilizer-projector family is
quadratic. That does not by itself prove that the known slope 2/3 is the best positive
linear coefficient. This script performs the missing census and then closes randomized
branch mixtures: the accepted-output slope of a mixture is a success-weighted convex
combination of constituent slopes.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sym

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2918_M36_FIRST_ORDER_CENSUS_results.json"
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j])


def kron(items):
    out = np.array([[1]], dtype=complex)
    for item in items:
        out = np.kron(out, item)
    return out


def projective_key(vector, digits=8):
    vector = np.asarray(vector, dtype=complex).reshape(-1)
    vector /= np.linalg.norm(vector)
    pivot = next(i for i, value in enumerate(vector) if abs(value) > 1e-9)
    vector /= vector[pivot] / abs(vector[pivot])
    return tuple((round(float(v.real), digits), round(float(v.imag), digits)) for v in vector)


def matrix_key(matrix, digits=8):
    flat = matrix.reshape(-1)
    pivot = next(i for i, value in enumerate(flat) if abs(value) > 1e-9)
    matrix = matrix / (flat[pivot] / abs(flat[pivot]))
    return tuple((round(float(v.real), digits), round(float(v.imag), digits)) for v in matrix.reshape(-1))


def two_qubit_cliffords():
    cx01 = np.zeros((4, 4), dtype=complex)
    cx10 = np.zeros((4, 4), dtype=complex)
    for a, b in itertools.product(range(2), repeat=2):
        cx01[2 * a + (b ^ a), 2 * a + b] = 1
        cx10[2 * (a ^ b) + b, 2 * a + b] = 1
    gens = [np.kron(H, I2), np.kron(I2, H), np.kron(S, I2), np.kron(I2, S), cx01, cx10]
    ident = np.eye(4, dtype=complex)
    seen = {matrix_key(ident): ident}
    queue = deque([ident])
    while queue:
        current = queue.popleft()
        for gen in gens:
            candidate = gen @ current
            key = matrix_key(candidate)
            if key not in seen:
                seen[key] = candidate
                queue.append(candidate)
    assert len(seen) == 11520
    return list(seen.values())


def rays():
    omega = np.exp(2j * np.pi / 3)
    result = []
    for family in range(4):
        for mu in range(3):
            for nu in range(3):
                raw = (
                    [0, 1, -omega**mu, omega**nu] if family == 0 else
                    [1, 0, -omega**mu, -omega**nu] if family == 1 else
                    [1, -omega**mu, 0, omega**nu] if family == 2 else
                    [1, omega**mu, omega**nu, 0]
                )
                result.append(np.asarray(raw, dtype=complex) / np.sqrt(3))
    return result


def bvec(integer):
    return tuple((integer >> bit) & 1 for bit in range(8))


def bxor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def symplectic(a, b):
    return sum(a[i] * b[4 + i] + a[4 + i] * b[i] for i in range(4)) % 2


def pauli(vector):
    return kron([
        (1j ** (x * z)) * np.linalg.matrix_power(X, x) @ np.linalg.matrix_power(Z, z)
        for x, z in zip(vector[:4], vector[4:])
    ])


PAULI = {bvec(i): pauli(bvec(i)) for i in range(256)}


def isotropic_spaces():
    vectors = [bvec(i) for i in range(1, 256)]
    spaces = set()
    for index, u in enumerate(vectors):
        for v in vectors[index + 1:]:
            if symplectic(u, v) == 0:
                spaces.add(tuple(sorted((u, v, bxor(u, v)))))
    assert len(spaces) == 5355
    return sorted(spaces)


def binary_span(basis):
    result = {(0,) * 8}
    for vector in basis:
        result |= {bxor(value, vector) for value in tuple(result)}
    return result


def extend_isotropic(s1, s2):
    basis = [s1, s2]
    span = binary_span(basis)
    for vector in [bvec(i) for i in range(1, 256)]:
        if vector not in span and all(symplectic(vector, member) == 0 for member in basis):
            basis.append(vector)
            span = binary_span(basis)
            if len(basis) == 4:
                return basis[2], basis[3]
    raise AssertionError("failed to extend isotropic basis")


def joint_eigenvector(operators, signs):
    projector = np.eye(16, dtype=complex)
    identity = np.eye(16, dtype=complex)
    for sign, operator in zip(signs, operators):
        projector = projector @ ((identity + sign * operator) / 2)
    column = int(np.argmax(np.linalg.norm(projector, axis=0)))
    vector = projector[:, column]
    vector /= np.linalg.norm(vector)
    pivot = next(i for i, value in enumerate(vector) if abs(value) > 1e-10)
    vector /= vector[pivot] / abs(vector[pivot])
    return vector


def syndrome_bases(space):
    s1, s2, _ = space
    l1, l2 = extend_isotropic(s1, s2)
    operators = [PAULI[value] for value in (s1, s2, l1, l2)]
    result = []
    for e1, e2 in itertools.product((1, -1), repeat=2):
        basis = np.column_stack([
            joint_eigenvector(operators, (e1, e2, z1, z2))
            for z1, z2 in itertools.product((1, -1), repeat=2)
        ])
        result.append(((e1, e2), basis))
    return result


def rational(value: float, max_denominator: int = 4096) -> str:
    frac = Fraction(float(value)).limit_denominator(max_denominator)
    if abs(float(frac) - float(value)) < 2e-8:
        return str(frac)
    radical = sym.nsimplify(value, [sym.sqrt(3)], tolerance=1e-9, full=True)
    if abs(float(sym.N(radical, 20)) - float(value)) < 2e-8:
        return str(radical)
    return f"{value:.12g}"


def class_orbit_keys(rr, cliffords, seed):
    return {projective_key(g @ rr[seed]) for g in cliffords}


def census_for_representative(label, ray, target_orbit_keys, spaces):
    pure = np.outer(ray, ray.conj())
    noise = np.eye(4) / 4 - pure
    c0 = np.kron(pure, pure)
    c1 = np.kron(pure, noise) + np.kron(noise, pure)
    slope_counter = Counter()
    closed = 0
    improving_linear = 0
    zero_slope = 0
    minimum = None
    minimum_records = []
    for code_index, space in enumerate(spaces):
        for syndrome, basis in syndrome_bases(space):
            l0 = basis.conj().T @ c0 @ basis
            q0 = float(np.trace(l0).real)
            if q0 < 1e-10:
                continue
            values, vectors = np.linalg.eigh(l0 / q0)
            if float(values[-1]) < 1 - 1e-8:
                continue
            target = vectors[:, -1]
            if projective_key(target) not in target_orbit_keys:
                continue
            l1 = basis.conj().T @ c1 @ basis
            q1 = float(np.trace(l1).real)
            n0 = float(np.vdot(target, l0 @ target).real)
            n1 = float(np.vdot(target, l1 @ target).real)
            assert abs(n0 - q0) < 2e-8
            slope = (4.0 / 3.0) * (q1 - n1) / q0
            if abs(slope) < 1e-8:
                slope = 0.0
            closed += 1
            slope_key = rational(slope)
            slope_counter[slope_key] += 1
            if slope < 1 - 1e-8:
                improving_linear += 1
            if slope == 0:
                zero_slope += 1
            if minimum is None or slope < minimum - 1e-9:
                minimum = slope
                minimum_records = [{"code_index": code_index, "syndrome": list(syndrome), "q0": rational(q0), "q1": rational(q1), "n1": rational(n1)}]
            elif abs(slope - minimum) < 1e-9 and len(minimum_records) < 12:
                minimum_records.append({"code_index": code_index, "syndrome": list(syndrome), "q0": rational(q0), "q1": rational(q1), "n1": rational(n1)})
    assert minimum is not None
    return {
        "label": label,
        "closed_branches": closed,
        "first_order_improving_branches": improving_linear,
        "zero_slope_branches": zero_slope,
        "minimum_p_out_slope": rational(minimum),
        "minimum_p_out_slope_decimal": minimum,
        "slope_histogram": dict(sorted(
            slope_counter.items(),
            key=lambda kv: float(sym.N(sym.sympify(kv[0], locals={"sqrt": sym.sqrt}), 20)),
        )),
        "minimum_witnesses": minimum_records,
    }


def main():
    rr = rays()
    cliffords = two_qubit_cliffords()
    spaces = isotropic_spaces()
    representatives = {"shallow": 0, "middle_a": 1, "middle_b": 2, "deep": 5}
    results = {}
    for label, seed in representatives.items():
        print(f"census {label} (seed {seed})...")
        results[label] = census_for_representative(
            label, rr[seed], class_orbit_keys(rr, cliffords, seed), spaces
        )
        print(results[label]["minimum_p_out_slope"], results[label]["first_order_improving_branches"])

    deep_min = results["deep"]["minimum_p_out_slope_decimal"]
    checks = {
        "clifford_order_11520": len(cliffords) == 11520,
        "codes_5355": len(spaces) == 5355,
        "no_zero_slope_any_class": all(item["zero_slope_branches"] == 0 for item in results.values()),
        "deep_has_first_order_improvements": results["deep"]["first_order_improving_branches"] > 0,
        "other_classes_no_first_order_improvements": sum(results[name]["first_order_improving_branches"] for name in ("shallow", "middle_a", "middle_b")) == 0,
        "known_two_thirds_is_global_minimum": abs(deep_min - 2 / 3) < 1e-8,
    }
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]

    output = {
        "schema": "w33.pass2918.m36_first_order_census.v1",
        "status": "COMPLETE_EXHAUSTIVE_FIRST_ORDER",
        "check_count": len(checks),
        "checks": checks,
        "class_results": results,
        "mixture_theorem": {
            "formula": "a_mix = sum_j w_j q0_j a_j / sum_j w_j q0_j",
            "consequence": "randomized accepted-output mixtures cannot beat the smallest constituent first-order slope",
            "adaptive_consequence": "any finite history-dependent composition of positive-slope branches remains linear; its leading coefficient is a positive product/mixture, never zero",
        },
        "headline": (
            "The exhaustive first-order census validates the previously over-strong wording: "
            "the global minimum two-copy stabilizer slope is 2/3, and success-weighted "
            "branch mixtures cannot improve it or cancel the linear term."
        ),
        "claim_boundary": (
            "This closes the full two-copy [[4,2]] stabilizer-projector family and its "
            "classical mixtures. It does not constrain three-copy protocols or non-stabilizer projections."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS {len(checks)}/{len(checks)}")
    print(output["headline"])


if __name__ == "__main__":
    main()
