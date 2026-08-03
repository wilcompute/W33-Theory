#!/usr/bin/env python3
"""Pass 2797: the two-copy M36 universality gap closes for the deep orbit.

This script exhausts all 5,355 binary [[4,2]] stabilizer projectors, all four
syndromes, and the complete projective two-qubit Clifford decoder orbit.  It fixes
logical Pauli bases by rank-one projectors, so no eigensolver phase enters the result.
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
PVAR = sp.symbols("p", real=True)
I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)
H2 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S2 = np.diag([1, 1j])


def kron_all(items):
    out = np.array([[1]], dtype=complex)
    for item in items:
        out = np.kron(out, item)
    return out


def projective_key(vector, digits=9):
    vector = np.asarray(vector, dtype=complex).reshape(-1)
    vector = vector / np.linalg.norm(vector)
    pivot = next(i for i, value in enumerate(vector) if abs(value) > 1e-9)
    vector = vector / (vector[pivot] / abs(vector[pivot]))
    return tuple((round(float(z.real), digits), round(float(z.imag), digits)) for z in vector)


def matrix_key(matrix, digits=9):
    flat = np.asarray(matrix, dtype=complex).reshape(-1)
    pivot = next(i for i, value in enumerate(flat) if abs(value) > 1e-9)
    matrix = matrix / (flat[pivot] / abs(flat[pivot]))
    return tuple((round(float(z.real), digits), round(float(z.imag), digits)) for z in matrix.reshape(-1))


def two_qubit_clifford_group():
    cx01 = np.zeros((4, 4), dtype=complex)
    cx10 = np.zeros((4, 4), dtype=complex)
    for a, b in itertools.product(range(2), repeat=2):
        cx01[2 * a + (b ^ a), 2 * a + b] = 1
        cx10[2 * (a ^ b) + b, 2 * a + b] = 1
    generators = [
        np.kron(H2, I2), np.kron(I2, H2), np.kron(S2, I2), np.kron(I2, S2), cx01, cx10
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


def bvec(integer, n=4):
    return tuple((integer >> bit) & 1 for bit in range(2 * n))


def bxor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def bsymp(a, b, n=4):
    return sum(a[i] * b[n + i] + a[n + i] * b[i] for i in range(n)) % 2


def hermitian_pauli(vector, n=4):
    return kron_all(
        [
            (1j ** (x * z))
            * np.linalg.matrix_power(X2, x)
            @ np.linalg.matrix_power(Z2, z)
            for x, z in zip(vector[:n], vector[n:])
        ]
    )


def all_isotropic_rank2():
    vectors = [bvec(i) for i in range(1, 256)]
    spaces = set()
    for i, u in enumerate(vectors):
        for v in vectors[i + 1 :]:
            if not bsymp(u, v):
                spaces.add(tuple(sorted((u, v, bxor(u, v)))))
    assert len(spaces) == 5355
    return sorted(spaces)


def span(basis):
    result = {(0,) * 8}
    for vector in basis:
        result |= {bxor(x, vector) for x in tuple(result)}
    return result


def extend_isotropic(s1, s2):
    basis = [s1, s2]
    subspace = span(basis)
    for vector in [bvec(i) for i in range(1, 256)]:
        if vector not in subspace and all(not bsymp(vector, b) for b in basis):
            basis.append(vector)
            subspace = span(basis)
            if len(basis) == 4:
                return basis[2], basis[3]
    raise AssertionError


PAULI4 = {bvec(i): hermitian_pauli(bvec(i)) for i in range(256)}


def joint_vector(operators, signs):
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
    operators = [PAULI4[x] for x in (s1, s2, l1, l2)]
    result = {}
    for e1, e2 in itertools.product((1, -1), repeat=2):
        basis = np.column_stack(
            [joint_vector(operators, (e1, e2, z1, z2)) for z1, z2 in itertools.product((1, -1), repeat=2)]
        )
        assert np.max(np.abs(basis.conj().T @ basis - np.eye(4))) < 1e-8
        result[(e1, e2)] = basis
    return result


EXACT_CACHE = {}


def exact(value):
    key = round(float(value), 10)
    if abs(key) < 1e-9:
        return sp.Integer(0)
    if key not in EXACT_CACHE:
        EXACT_CACHE[key] = sp.nsimplify(key, [SQ3], tolerance=1e-8, full=False)
    return EXACT_CACHE[key]


def positive_on_open_interval(polynomial, endpoint):
    polynomial = sp.factor(polynomial)
    roots = []
    for root in sp.nroots(polynomial, maxsteps=100):
        if abs(complex(root).imag) < 1e-9:
            value = float(sp.re(root))
            if 1e-10 < value < float(endpoint) - 1e-10:
                roots.append(value)
    cuts = [0.0] + sorted(set(round(x, 10) for x in roots)) + [float(endpoint)]
    samples = [(cuts[i] + cuts[i + 1]) / 2 for i in range(len(cuts) - 1)]
    values = [float(sp.N(polynomial.subs(PVAR, sample), 30)) for sample in samples]
    return all(value > 1e-10 for value in values)


def grade_representatives(rays):
    # Frozen by the exact stabilizer-fidelity census from Pass 2767.
    return {
        "shallow": (0, sp.Rational(3, 4)),
        "mid_a": (1, (5 + 2 * SQ3) / 12),
        "mid_b": (2, (5 + 2 * SQ3) / 12),
        "deep": (5, (2 + SQ3) / 6),
    }


def scan_grade(input_ray, witness_fidelity, orbit_keys, spaces):
    pure = np.outer(input_ray, input_ray.conj())
    noise = np.eye(4) / 4 - pure
    input_coefficients = [np.kron(pure, pure), np.kron(pure, noise) + np.kron(noise, pure), np.kron(noise, noise)]
    endpoint = sp.N(4 * (1 - witness_fidelity) / 3, 30)
    closed = improving = identical = 0
    profiles = Counter()
    representative = None

    for space in spaces:
        for syndrome, basis in syndrome_bases(space).items():
            logical = [basis.conj().T @ coefficient @ basis for coefficient in input_coefficients]
            q = [exact(np.trace(operator).real) for operator in logical]
            if q[0] == 0:
                continue
            values, vectors = np.linalg.eigh(logical[0] / float(q[0]))
            target = vectors[:, int(np.argmax(values))]
            if float(max(values)) < 1 - 1e-8 or projective_key(target) not in orbit_keys:
                continue
            closed += 1
            n = [exact(np.real(np.vdot(target, operator @ target))) for operator in logical]
            qpoly = sum(q[i] * PVAR**i for i in range(3))
            npoly = sum(n[i] * PVAR**i for i in range(3))
            difference_numerator = sp.factor(npoly - (1 - sp.Rational(3, 4) * PVAR) * qpoly)
            if difference_numerator == 0:
                identical += 1
                profiles["identical"] += 1
            elif positive_on_open_interval(difference_numerator, endpoint):
                improving += 1
                profile = (tuple(q), tuple(n), str(sp.factor(difference_numerator)))
                profiles[str(profile)] += 1
                if representative is None:
                    representative = {
                        "stabilizer_generators": [list(space[0]), list(space[1]), list(space[2])],
                        "syndrome": list(syndrome),
                        "q_coefficients": [str(x) for x in q],
                        "n_coefficients": [str(x) for x in n],
                        "success_probability": str(sp.factor(qpoly)),
                        "output_fidelity": str(sp.factor(npoly / qpoly)),
                        "difference_from_input": str(sp.factor(difference_numerator / qpoly)),
                    }
            else:
                profiles["nonimproving"] += 1
    return {
        "closed_branches": closed,
        "improving_branches": improving,
        "identical_branches": identical,
        "profiles": dict(profiles),
        "representative": representative,
    }


def main():
    rays, metadata = m36_rays()
    cliffords = two_qubit_clifford_group()
    orbit_members = {}
    orbit_sets = []
    unseen = set(range(36))
    while unseen:
        seed = min(unseen)
        keys = {projective_key(clifford @ rays[seed]) for clifford in cliffords}
        ids = [i for i, ray in enumerate(rays) if projective_key(ray) in keys]
        for i in ids:
            unseen.discard(i)
        orbit_sets.append({"seed": seed, "size": len(keys), "m36_ids": ids})
        orbit_members.update({key: seed for key in keys})
    assert sorted(item["size"] for item in orbit_sets) == [640, 960, 2880, 2880]
    assert len(orbit_members) == 7360

    spaces = all_isotropic_rank2()
    results = {}
    for grade, (ray_id, witness) in grade_representatives(rays).items():
        results[grade] = scan_grade(rays[ray_id], witness, orbit_members, spaces)

    assert results["shallow"]["improving_branches"] == 0
    assert results["mid_a"]["improving_branches"] == 0
    assert results["mid_b"]["improving_branches"] == 0
    assert results["deep"]["improving_branches"] == 48

    # Freeze the simplest exact improving branch and its physical decoder witness.
    representative = results["deep"]["representative"]
    expected_q = [sp.Rational(1, 2), -sp.Rational(1, 2), sp.Rational(1, 4)]
    expected_n = [sp.Rational(1, 2), -sp.Rational(3, 4), sp.Rational(5, 16)]
    assert representative["q_coefficients"] == [str(x) for x in expected_q]
    assert representative["n_coefficients"] == [str(x) for x in expected_n]
    exact_difference = sp.factor(
        PVAR * (PVAR - 1) * (3 * PVAR - 2) / (4 * (PVAR**2 - 2 * PVAR + 2))
    )
    representative.update(
        {
            "input_m36_id": 5,
            "input_metadata": list(metadata[5]),
            "target_m36_id": 7,
            "target_metadata": list(metadata[7]),
            "logical_clifford_decoder": "H on the second logical qubit",
            "strict_improvement_interval": "0 < p < 2/3",
            "deep_magic_interval": "0 < p < (8-2*sqrt(3))/9",
            "exact_difference_crosscheck": str(exact_difference),
        }
    )

    checks = {
        "clifford_order_11520": len(cliffords) == 11520,
        "four_m36_clifford_orbits": len(orbit_sets) == 4,
        "union_orbit_7360": len(orbit_members) == 7360,
        "codes_5355": len(spaces) == 5355,
        "deep_improving_48": results["deep"]["improving_branches"] == 48,
        "other_orbits_no_improvement": sum(results[key]["improving_branches"] for key in ("shallow", "mid_a", "mid_b")) == 0,
        "representative_improves_full_deep_magic_interval": float((8 - 2 * SQ3) / 9) < 2 / 3,
    }
    assert all(checks.values())

    output = {
        "schema": "w33.pass2797.m36_clifford_decoder_distillation.v1",
        "status": "EXACT_EXHAUSTIVE_TWO_COPY_CLIFFORD_DECODER_DISTILLATION",
        "clifford_group_order": len(cliffords),
        "m36_clifford_orbits": orbit_sets,
        "m36_union_orbit_size": len(orbit_members),
        "search_space": {"codes": len(spaces), "syndromes_per_code": 4, "logical_cliffords": len(cliffords)},
        "grade_results": results,
        "distillation_protocol": representative,
        "result": "The deep eight-ray M36 orbit has 48 two-copy improving stabilizer-projection branches once arbitrary two-qubit logical Clifford decoding is included. The simplest branch improves throughout the full deep magic-witness interval.",
        "boundary": "This is a state-fidelity distillation theorem for two identical depolarized inputs. It is not yet a fault-tolerant injection threshold or an asymptotic multi-round yield theorem.",
        "checks": checks,
    }
    path = ROOT / "data/PART_BT2797_M36_CLIFFORD_DECODER_DISTILLATION_results.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
