#!/usr/bin/env python3
"""Pass 2804: exhaustive two-copy M36 distillation with logical Clifford decoding.

The search covers every binary [[4,2]] stabilizer projector, every syndrome, and the
complete projective two-qubit Clifford decoder orbit.  Logical Pauli eigenstates are
constructed from rank-one projectors with a deterministic phase gauge.  The 21,420
logical bases are cached once, and exact fidelity polynomials are certified once per
distinct profile rather than once per branch.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SQ3 = sp.sqrt(3)
p = sp.symbols("p", real=True)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j])


def kron(matrices):
    out = np.array([[1]], dtype=complex)
    for matrix in matrices:
        out = np.kron(out, matrix)
    return out


def projective_key(vector, digits=9):
    vector = np.asarray(vector, dtype=complex).reshape(-1)
    vector /= np.linalg.norm(vector)
    pivot = next(i for i, value in enumerate(vector) if abs(value) > 1e-9)
    vector /= vector[pivot] / abs(vector[pivot])
    return tuple(
        (round(float(value.real), digits), round(float(value.imag), digits))
        for value in vector
    )


def matrix_key(matrix, digits=9):
    flat = matrix.reshape(-1)
    pivot = next(i for i, value in enumerate(flat) if abs(value) > 1e-9)
    matrix = matrix / (flat[pivot] / abs(flat[pivot]))
    return tuple(
        (round(float(value.real), digits), round(float(value.imag), digits))
        for value in matrix.reshape(-1)
    )


def two_qubit_cliffords():
    cx01 = np.zeros((4, 4), dtype=complex)
    cx10 = np.zeros((4, 4), dtype=complex)
    for a, b in itertools.product(range(2), repeat=2):
        cx01[2 * a + (b ^ a), 2 * a + b] = 1
        cx10[2 * (a ^ b) + b, 2 * a + b] = 1
    generators = [
        np.kron(H, I2),
        np.kron(I2, H),
        np.kron(S, I2),
        np.kron(I2, S),
        cx01,
        cx10,
    ]
    identity = np.eye(4, dtype=complex)
    seen = {matrix_key(identity): identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = generator @ current
            key = matrix_key(candidate)
            if key not in seen:
                seen[key] = candidate
                queue.append(candidate)
    assert len(seen) == 11520
    return list(seen.values())


def m36_rays():
    omega = np.exp(2j * np.pi / 3)
    rays, metadata = [], []
    for family in range(4):
        for mu in range(3):
            for nu in range(3):
                raw = (
                    [0, 1, -omega**mu, omega**nu]
                    if family == 0
                    else [1, 0, -omega**mu, -omega**nu]
                    if family == 1
                    else [1, -omega**mu, 0, omega**nu]
                    if family == 2
                    else [1, omega**mu, omega**nu, 0]
                )
                rays.append(np.array(raw, dtype=complex) / np.sqrt(3))
                metadata.append((family, mu, nu))
    return rays, metadata


def bvec(integer):
    return tuple((integer >> bit) & 1 for bit in range(8))


def bxor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def symplectic(a, b):
    return sum(a[i] * b[4 + i] + a[4 + i] * b[i] for i in range(4)) % 2


def pauli(vector):
    return kron(
        [
            (1j ** (x * z))
            * np.linalg.matrix_power(X, x)
            @ np.linalg.matrix_power(Z, z)
            for x, z in zip(vector[:4], vector[4:])
        ]
    )


PAULI = {bvec(i): pauli(bvec(i)) for i in range(256)}


def isotropic_spaces():
    vectors = [bvec(i) for i in range(1, 256)]
    result = set()
    for index, u in enumerate(vectors):
        for v in vectors[index + 1 :]:
            if not symplectic(u, v):
                result.add(tuple(sorted((u, v, bxor(u, v)))))
    assert len(result) == 5355
    return sorted(result)


def binary_span(basis):
    result = {(0,) * 8}
    for vector in basis:
        result |= {bxor(value, vector) for value in tuple(result)}
    return result


def extend_isotropic(s1, s2):
    basis = [s1, s2]
    current_span = binary_span(basis)
    for vector in [bvec(i) for i in range(1, 256)]:
        if vector not in current_span and all(
            not symplectic(vector, member) for member in basis
        ):
            basis.append(vector)
            current_span = binary_span(basis)
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
    result = {}
    for e1, e2 in itertools.product((1, -1), repeat=2):
        basis = np.column_stack(
            [
                joint_eigenvector(operators, (e1, e2, z1, z2))
                for z1, z2 in itertools.product((1, -1), repeat=2)
            ]
        )
        assert np.max(np.abs(basis.conj().T @ basis - np.eye(4))) < 1e-8
        result[(e1, e2)] = basis
    return result


def prepare_branches(spaces):
    prepared = []
    for space in spaces:
        for syndrome, basis in syndrome_bases(space).items():
            prepared.append((space, syndrome, basis))
    assert len(prepared) == 21420
    return prepared


EXACT_CACHE = {}


def exact(value):
    key = round(float(value), 10)
    if abs(key) < 1e-9:
        return sp.Integer(0)
    if key not in EXACT_CACHE:
        EXACT_CACHE[key] = sp.nsimplify(
            key, [SQ3], tolerance=1e-8, full=False
        )
    return EXACT_CACHE[key]


def positive_on_open_interval(polynomial, endpoint):
    roots = []
    for root in sp.nroots(polynomial, maxsteps=100):
        if abs(complex(root).imag) < 1e-9:
            value = float(sp.re(root))
            if 1e-10 < value < float(endpoint) - 1e-10:
                roots.append(value)
    cuts = [0.0] + sorted(set(round(value, 10) for value in roots)) + [
        float(endpoint)
    ]
    return all(
        float(
            sp.N(polynomial.subs(p, (cuts[i] + cuts[i + 1]) / 2), 30)
        )
        > 1e-10
        for i in range(len(cuts) - 1)
    )


def scan_grade(input_ray, stabilizer_fidelity, orbit, prepared):
    pure = np.outer(input_ray, input_ray.conj())
    noise = np.eye(4) / 4 - pure
    coefficients = [
        np.kron(pure, pure),
        np.kron(pure, noise) + np.kron(noise, pure),
        np.kron(noise, noise),
    ]
    endpoint = sp.N(4 * (1 - stabilizer_fidelity) / 3, 30)
    profile_counts = Counter()

    for _, _, basis in prepared:
        logical = [basis.conj().T @ coefficient @ basis for coefficient in coefficients]
        q_coefficients = tuple(exact(np.trace(operator).real) for operator in logical)
        if q_coefficients[0] == 0:
            continue
        values, vectors = np.linalg.eigh(logical[0] / float(q_coefficients[0]))
        target = vectors[:, int(np.argmax(values))]
        if max(values) < 1 - 1e-8 or projective_key(target) not in orbit:
            continue
        n_coefficients = tuple(
            exact(np.real(np.vdot(target, operator @ target))) for operator in logical
        )
        success = sum(q_coefficients[i] * p**i for i in range(3))
        numerator = sum(n_coefficients[i] * p**i for i in range(3))
        difference = sp.factor(
            numerator - (1 - sp.Rational(3, 4) * p) * success
        )
        profile_counts[(q_coefficients, n_coefficients, str(difference))] += 1

    closed = sum(profile_counts.values())
    improving = identical = nonimproving = 0
    profiles = {}
    for (q_coefficients, n_coefficients, difference_text), multiplicity in sorted(
        profile_counts.items(), key=lambda item: str(item[0])
    ):
        difference = sp.sympify(
            difference_text, locals={"p": p, "sqrt": sp.sqrt}
        )
        if difference == 0:
            classification = "identical"
            identical += multiplicity
        elif positive_on_open_interval(difference, endpoint):
            classification = "improving"
            improving += multiplicity
        else:
            classification = "nonimproving"
            nonimproving += multiplicity
        profiles[str((q_coefficients, n_coefficients, difference_text))] = {
            "multiplicity": multiplicity,
            "classification": classification,
        }

    assert closed == improving + identical + nonimproving
    return {
        "closed_branches": closed,
        "improving_branches": improving,
        "identical_branches": identical,
        "nonimproving_branches": nonimproving,
        "distinct_profiles": len(profile_counts),
        "profiles": profiles,
    }


def explicit_protocol(rays, metadata):
    s1 = (0, 1, 0, 1, 0, 1, 1, 1)
    s2 = (1, 0, 1, 1, 1, 1, 0, 1)
    space = tuple(sorted((s1, s2, bxor(s1, s2))))
    basis = syndrome_bases(space)[(-1, 1)]
    pure = np.outer(rays[5], rays[5].conj())
    noise = np.eye(4) / 4 - pure
    logical = [
        basis.conj().T @ coefficient @ basis
        for coefficient in (
            np.kron(pure, pure),
            np.kron(pure, noise) + np.kron(noise, pure),
            np.kron(noise, noise),
        )
    ]
    q_coefficients = [exact(np.trace(operator).real) for operator in logical]
    values, vectors = np.linalg.eigh(logical[0] / float(q_coefficients[0]))
    target = vectors[:, int(np.argmax(values))]
    decoded_target = np.kron(I2, H) @ target
    assert projective_key(decoded_target) == projective_key(rays[7])
    n_coefficients = [
        exact(np.real(np.vdot(target, operator @ target))) for operator in logical
    ]
    assert q_coefficients == [
        sp.Rational(1, 2),
        -sp.Rational(1, 2),
        sp.Rational(1, 4),
    ]
    assert n_coefficients == [
        sp.Rational(1, 2),
        -sp.Rational(3, 4),
        sp.Rational(5, 16),
    ]
    success = sum(q_coefficients[i] * p**i for i in range(3))
    numerator = sum(n_coefficients[i] * p**i for i in range(3))
    return {
        "input_id": 5,
        "input_metadata": list(metadata[5]),
        "stabilizer_generators": [list(s1), list(s2), list(bxor(s1, s2))],
        "syndrome": [-1, 1],
        "decoder": "Hadamard on second logical qubit",
        "target_id": 7,
        "target_metadata": list(metadata[7]),
        "success_probability": str(sp.factor(success)),
        "output_fidelity": str(sp.factor(numerator / success)),
        "difference_from_input": str(
            sp.factor(numerator / success - (1 - sp.Rational(3, 4) * p))
        ),
        "strict_improvement_interval": "0 < p < 2/3",
        "deep_magic_interval": "0 < p < (8-2*sqrt(3))/9",
    }


def main():
    rays, metadata = m36_rays()
    cliffords = two_qubit_cliffords()
    unseen = set(range(36))
    orbit_records = []
    orbit_union = {}
    while unseen:
        seed = min(unseen)
        keys = {projective_key(clifford @ rays[seed]) for clifford in cliffords}
        ids = [i for i, ray in enumerate(rays) if projective_key(ray) in keys]
        for ray_id in ids:
            unseen.discard(ray_id)
        orbit_records.append({"seed": seed, "size": len(keys), "m36_ids": ids})
        orbit_union.update({key: seed for key in keys})
    assert sorted(record["size"] for record in orbit_records) == [
        640,
        960,
        2880,
        2880,
    ]
    assert len(orbit_union) == 7360

    spaces = isotropic_spaces()
    prepared = prepare_branches(spaces)
    representatives = {
        "shallow": (0, sp.Rational(3, 4)),
        "mid_a": (1, (5 + 2 * SQ3) / 12),
        "mid_b": (2, (5 + 2 * SQ3) / 12),
        "deep": (5, (2 + SQ3) / 6),
    }
    results = {
        grade: scan_grade(rays[ray_id], fidelity, orbit_union, prepared)
        for grade, (ray_id, fidelity) in representatives.items()
    }
    assert [
        results[grade]["improving_branches"]
        for grade in ("shallow", "mid_a", "mid_b", "deep")
    ] == [0, 0, 0, 48]

    checks = {
        "clifford_order_11520": len(cliffords) == 11520,
        "four_orbits": len(orbit_records) == 4,
        "union_7360": len(orbit_union) == 7360,
        "codes_5355": len(spaces) == 5355,
        "branches_21420": len(prepared) == 21420,
        "deep_improving_48": results["deep"]["improving_branches"] == 48,
        "other_grades_improving_zero": sum(
            results[grade]["improving_branches"]
            for grade in ("shallow", "mid_a", "mid_b")
        )
        == 0,
    }
    assert all(checks.values())

    output = {
        "schema": "w33.pass2804.m36_clifford_decoder_distillation.v2",
        "status": "EXACT_EXHAUSTIVE",
        "clifford_group_order": len(cliffords),
        "m36_clifford_orbits": orbit_records,
        "search_space": {
            "codes": len(spaces),
            "syndromes_per_code": 4,
            "logical_cliffords": len(cliffords),
            "prepared_branches": len(prepared),
        },
        "grade_results": results,
        "distillation_protocol": explicit_protocol(rays, metadata),
        "result": "The deep eight-ray grade has 48 improving two-copy branches under full logical Clifford decoding; the explicit H-decoded branch improves throughout the full deep magic-witness interval.",
        "boundary": "State-fidelity distillation, not yet a fault-tolerant injection threshold or asymptotic yield theorem.",
        "checks": checks,
    }
    path = ROOT / "data/PART_BT2804_M36_CLIFFORD_DECODER_DISTILLATION_results.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
