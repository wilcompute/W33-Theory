#!/usr/bin/env python3
"""Pass 2784: deterministic [[4,2]] binary-stabilizer projection census.

The original implementation diagonalized a nondegenerate Pauli-label Hamiltonian with
``numpy.linalg.eigh`` and then used the returned eigenvector phases as logical basis
phases.  Those phases are mathematically arbitrary, so the number of branches whose
logical output landed on an M36 ray changed across LAPACK/NumPy builds.  This version
constructs each joint Pauli eigenvector directly from its rank-one projector and fixes
its phase by a deterministic pivot convention.

The resulting statement is deliberately narrower than the earlier draft: it covers the
canonical logical Pauli frame and this explicit phase gauge.  It does not silently absorb
arbitrary logical Clifford decoders.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp

from bt2777_2781_core import *

ROOT = Path(__file__).resolve().parents[1]
SQ3 = sp.sqrt(3)
p = sp.symbols("p", real=True)


def all_isotropic_rank2():
    vecs = [bvec(i, 4) for i in range(1, 256)]
    out = set()
    for i, u in enumerate(vecs):
        for v in vecs[i + 1 :]:
            if not bsymp(u, v, 4):
                out.add(tuple(sorted((u, v, bxor(u, v)))))
    assert len(out) == 5355
    return sorted(out)


def span(basis):
    out = {(0,) * 8}
    for b in basis:
        out |= {bxor(x, b) for x in tuple(out)}
    return out


def extend_iso(s1, s2):
    basis = [s1, s2]
    subspace = span(basis)
    for v in [bvec(i, 4) for i in range(1, 256)]:
        if v not in subspace and all(not bsymp(v, b, 4) for b in basis):
            basis.append(v)
            subspace = span(basis)
            if len(basis) == 4:
                return basis[2], basis[3]
    raise AssertionError("failed to extend isotropic basis")


PAULI4 = {bvec(i, 4): hermitian_pauli(bvec(i, 4), 4) for i in range(256)}


def canonical_joint_eigenvector(operators, signs):
    """Return the deterministically phased rank-one joint eigenvector.

    For commuting Hermitian involutions P_i, the product

        prod_i (I + sign_i P_i)/2

    is the rank-one projector onto the requested joint eigenspace.  Selecting the
    projector column with largest norm and making its first nonzero component positive
    real fixes all LAPACK-independent basis and phase choices.
    """

    dim = operators[0].shape[0]
    projector = np.eye(dim, dtype=complex)
    eye = np.eye(dim, dtype=complex)
    for sign, operator in zip(signs, operators):
        projector = projector @ ((eye + sign * operator) / 2)

    hermitian_residual = np.max(np.abs(projector - projector.conj().T))
    idempotent_residual = np.max(np.abs(projector @ projector - projector))
    trace = np.trace(projector).real
    assert hermitian_residual < 1e-9
    assert idempotent_residual < 1e-9
    assert abs(trace - 1.0) < 1e-9

    column_norms = np.linalg.norm(projector, axis=0)
    column = int(np.argmax(column_norms))
    vector = projector[:, column]
    vector /= np.linalg.norm(vector)

    pivots = np.flatnonzero(np.abs(vector) > 1e-10)
    assert len(pivots)
    pivot = int(pivots[0])
    vector /= vector[pivot] / abs(vector[pivot])
    assert abs(vector[pivot].imag) < 1e-9 and vector[pivot].real > 0
    return vector


def syndrome_bases(sub):
    s1, s2, _ = sub
    l1, l2 = extend_iso(s1, s2)
    operators = [PAULI4[x] for x in (s1, s2, l1, l2)]
    out = {}
    for e1, e2 in itertools.product((1, -1), repeat=2):
        columns = []
        for z1, z2 in itertools.product((1, -1), repeat=2):
            columns.append(
                canonical_joint_eigenvector(operators, (e1, e2, z1, z2))
            )
        basis = np.column_stack(columns)
        assert np.max(np.abs(basis.conj().T @ basis - np.eye(4))) < 1e-9
        out[(e1, e2)] = basis
    return out


_EXACT_CACHE = {}


def exact(x):
    key = round(float(x), 11)
    if abs(key) < 1e-10:
        return sp.Integer(0)
    if key not in _EXACT_CACHE:
        _EXACT_CACHE[key] = sp.nsimplify(key, [SQ3], tolerance=1e-8, full=False)
    return _EXACT_CACHE[key]


def bernstein_power_to_coeff(a):
    a = list(a) + [0] * (4 - len(a))
    a0, a1, a2, a3 = a[:4]
    return [
        a0,
        a0 + a1 / 3,
        a0 + 2 * a1 / 3 + a2 / 3,
        a0 + a1 + a2 + a3,
    ]


def subdivide_bernstein(b):
    levels = [list(b)]
    while len(levels[-1]) > 1:
        levels.append(
            [
                (levels[-1][i] + levels[-1][i + 1]) / 2
                for i in range(len(levels[-1]) - 1)
            ]
        )
    return [levels[i][0] for i in range(4)], [levels[3 - i][i] for i in range(4)]


def nonpositive_bernstein(b, depth=0):
    if all(sp.simplify(x) <= 0 for x in b):
        return True
    if depth >= 18:
        return False
    left, right = subdivide_bernstein(b)
    return nonpositive_bernstein(left, depth + 1) and nonpositive_bernstein(
        right, depth + 1
    )


def certify_poly(dcoef, pmax):
    scaled = [sp.simplify(dcoef[i] * pmax**i) for i in range(4)]
    return nonpositive_bernstein(bernstein_power_to_coeff(scaled))


def ray_expect(operator, rays):
    return np.real(np.einsum("ij,ji->i", rays.conj().T @ operator, rays))


def census(psi, fstab, rays, subs):
    pure = np.outer(psi, psi.conj())
    noise = np.eye(4) / 4 - pure
    coefficients = [
        np.kron(pure, pure),
        np.kron(pure, noise) + np.kron(noise, pure),
        np.kron(noise, noise),
    ]
    ray_matrix = np.column_stack(rays)
    pmax = sp.nsimplify(4 * (1 - fstab) / 3, [SQ3])
    closure = certified = identical = 0
    profiles = Counter()
    worst = None

    for sub in subs:
        for syndrome, basis in syndrome_bases(sub).items():
            logical_coefficients = [basis.conj().T @ c @ basis for c in coefficients]
            trace_coefficients = [float(np.trace(x).real) for x in logical_coefficients]
            if trace_coefficients[0] < 1e-12:
                continue

            numerators = np.stack(
                [ray_expect(x, ray_matrix) for x in logical_coefficients], axis=1
            )
            targets = np.where(
                numerators[:, 0] / trace_coefficients[0] > 1 - 1e-8
            )[0]
            if not len(targets):
                continue

            q = [exact(x) for x in trace_coefficients]
            for target_index in targets:
                closure += 1
                n = [exact(x) for x in numerators[target_index]]
                difference = [sp.Integer(0)] * 4
                for i in range(3):
                    difference[i] += n[i] - q[i]
                for i in range(3):
                    difference[i + 1] += sp.Rational(3, 4) * q[i]
                difference = [sp.simplify(x) for x in difference]

                if all(x == 0 for x in difference):
                    identical += 1
                    certified += 1
                    profiles["identical_fidelity"] += 1
                    continue

                if not certify_poly(difference, pmax):
                    raise AssertionError(
                        (fstab, sub, syndrome, target_index, difference, pmax)
                    )
                certified += 1
                lead = next(i for i, x in enumerate(difference) if x != 0)
                profiles[f"first_negative_order_{lead}"] += 1
                midpoint = sp.N(
                    sum(difference[i] * (pmax / 2) ** i for i in range(4)), 30
                )
                if worst is None or midpoint > worst[0]:
                    worst = (midpoint, difference)

    assert closure == certified
    return {
        "nearest_stabilizer_fidelity_exact": str(fstab),
        "magic_witness_p_max_exact": str(pmax),
        "codes": 5355,
        "syndromes_per_code": 4,
        "m36_closed_branches": closure,
        "certified_nonimproving_branches": certified,
        "fidelity_identical_branches": identical,
        "polynomial_profiles": dict(profiles),
        "best_nontrivial_midpoint_difference": str(worst[0]) if worst else None,
        "best_nontrivial_difference_polynomial": (
            str(sp.Poly(sum(worst[1][i] * p**i for i in range(4)), p).as_expr())
            if worst
            else None
        ),
    }


def fanout_formula(k):
    ds = (4 - p) / 12
    dd = p / 4
    fidelity = sp.simplify((ds**k + 2 * (1 - p) ** k / 3**k) / (3 * ds**k + dd**k))
    return {
        "copies": k,
        "success_probability": str(sp.factor(3 * ds**k + dd**k)),
        "output_fidelity": str(sp.factor(fidelity)),
        "difference_from_input": str(
            sp.factor(fidelity - (1 - sp.Rational(3, 4) * p))
        ),
    }


def main():
    rays, _, groups = m36_grade_data()
    subs = all_isotropic_rank2()
    exact_f = {
        8: (2 + SQ3) / 6,
        24: (5 + 2 * SQ3) / 12,
        4: sp.Rational(3, 4),
    }
    rows = []
    for _, ids in sorted(groups.items(), key=lambda item: len(item[1])):
        size = len(ids)
        row = census(rays[ids[0]], exact_f[size], rays, subs)
        row["grade"] = {8: "deep", 24: "mid", 4: "shallow"}[size]
        row["grade_size"] = size
        rows.append(row)

    decoder_gauge = {
        "logical_frame": "deterministic symplectic extension by lexicographic Pauli vectors",
        "basis": "rank-one joint Pauli projectors",
        "phase": "first nonzero computational component positive real",
        "arbitrary_logical_clifford_exhausted": False,
    }
    out = {
        "schema": "w33.pass2784.m36_4_2_stabilizer_census.v2",
        "status": "EXACT_CANONICAL_DECODER_NO_GO",
        "search_space": {
            "input": "two identical depolarized M36 resources",
            "protocols": "all binary [[4,2]] stabilizer projectors and all four syndromes in the frozen canonical logical Pauli decoder gauge",
            "isotropic_rank2_codes": 5355,
            "branches": 21420,
        },
        "decoder_gauge": decoder_gauge,
        "rows": rows,
        "natural_fanout_recurrences": [fanout_formula(k) for k in range(2, 7)],
        "result": "No M36-closed branch in the frozen canonical logical Pauli decoder gauge strictly improves depolarizing fidelity anywhere inside its grade-specific magic-witness interval.",
        "boundary": "This is exhaustive for all two-copy binary [[4,2]] stabilizer projectors and syndromes only after fixing the stated logical Pauli basis and phase convention. It does not exhaust arbitrary logical Clifford decoders, larger block codes, nonidentical inputs, catalytic resources, adaptive multi-round protocols, or non-stabilizer assistance.",
    }
    path = ROOT / "data/PART_BT2777_M36_4_2_STABILIZER_CENSUS.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    summary = {
        key: out[key]
        for key in (
            "schema",
            "status",
            "search_space",
            "decoder_gauge",
            "result",
            "rows",
            "boundary",
        )
    }
    (ROOT / "data/PART_BT2777_M36_4_2_STABILIZER_CENSUS_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print("wrote", path)


if __name__ == "__main__":
    main()
