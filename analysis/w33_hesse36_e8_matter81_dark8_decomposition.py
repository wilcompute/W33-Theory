#!/usr/bin/env python3
"""Decompose the 8-dimensional dark complement of the 81x270 cubic incidence.

The September-23 root-lift boundary proves that the full lifted cubic incidence
matrix on K=H27_address x C3_external has rank 73, hence an 8-dimensional
left-kernel in the 81-dimensional root/address carrier.

This file identifies that dark K-module exactly.

Let H27 use normal form (a,b,c)=Z^a X^b omega^c with
    (a,b,c)(A,B,C)=(a+A,b+B,c+C-bA).
Let K=H27 x C3_external.  The 270 instruction columns are the right cosets of
the ten lifted order-three directions: the five selected H27 directions with
external slopes +/-1.

The left regular K-action preserves the incidence kernel.  Exact rational
linear algebra gives its character and decomposition:

    dark8
      = chi_ext + chi_ext^2
        + V_omega + V_omega^2,

where chi_ext is the nontrivial 1D character of the external C3, and V_omega,
V_omega^2 are the two 3D H27 Schroedinger irreps with trivial external
character.  Dimensions: 1+1+3+3=8.

This sharpens the rank-73 boundary: a future 81-root compiler must supply these
four irreducible sectors; cubic incidence alone cannot see them.

Boundary: the repeated numeral 8 is not identified with the E8 Cartan.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, zeros

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_hesse36_e8_matter81_dark8_decomposition.json"

F = range(3)
H = tuple(itertools.product(F, repeat=3))
ID = (0, 0, 0)
KID = (ID, 0)

DIRECTIONS = (
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
    (1, 2, 2),
)


def hmul(g, h):
    a, b, c = g
    A, B, C = h
    return ((a + A) % 3, (b + B) % 3, (c + C - b * A) % 3)


K = tuple((g, p) for g in H for p in F)


def kmul(x, y):
    return (hmul(x[0], y[0]), (x[1] + y[1]) % 3)


def right_cosets(group, subgroup):
    unseen = set(group)
    out = []
    while unseen:
        g = min(unseen)
        coset = frozenset(kmul(g, h) for h in subgroup)
        out.append(coset)
        unseen -= coset
    return out


def lifted_lines():
    out = []
    for d in DIRECTIONS:
        for slope in (1, 2):
            generator = (d, slope)
            subgroup = frozenset((KID, generator, kmul(generator, generator)))
            assert len(subgroup) == 3
            cosets = right_cosets(K, subgroup)
            assert len(cosets) == 27
            out.extend(cosets)
    assert len(out) == len(set(out)) == 270
    return out


def omega_sum_to_pair(counts):
    """c0+c1*w+c2*w^2 -> (A,B) for A+B*w, w^2=-1-w."""
    c0, c1, c2 = counts
    return (c0 - c2, c1 - c2)


def character_inner_multiplicity(traces, exponent_fn, scalar=1, support_fn=None):
    """Exact <dark,chi> for chi=scalar*w^exponent on optional support."""
    counts = [0, 0, 0]
    for x, tr in traces.items():
        if support_fn is not None and not support_fn(x):
            continue
        exponent = (-exponent_fn(x)) % 3  # complex conjugate
        counts[exponent] += int(tr) * scalar
    A, B = omega_sum_to_pair(counts)
    assert B == 0
    assert A % 81 == 0
    return A // 81


def main(write=True):
    lines = lifted_lines()
    Klist = list(K)
    index = {x: i for i, x in enumerate(Klist)}

    incidence = zeros(81, 270)
    for j, line in enumerate(lines):
        for x in line:
            incidence[index[x], j] = 1

    rank = incidence.rank()
    assert rank == 73
    null = incidence.T.nullspace()
    assert len(null) == 8
    basis = Matrix.hstack(*null)
    assert basis.shape == (81, 8)
    assert basis.rank() == 8

    # Pick eight rows giving an invertible coordinate minor.
    _, pivot_rows = basis.T.rref()
    pivot_rows = list(pivot_rows)
    assert len(pivot_rows) == 8
    minor = basis.extract(pivot_rows, list(range(8)))
    assert minor.det() != 0
    minor_inv = minor.inv()

    traces = {}
    invariant = True
    for g in Klist:
        moved = zeros(81, 8)
        for x in Klist:
            y = kmul(g, x)
            moved[index[y], :] = basis[index[x], :]
        if incidence.T * moved != zeros(270, 8):
            invariant = False
            break
        restricted = minor_inv * moved.extract(pivot_rows, list(range(8)))
        assert basis * restricted == moved
        tr = restricted.trace()
        assert tr.q == 1
        traces[g] = int(tr)
    assert invariant and len(traces) == 81

    trace_hist = Counter(traces.values())
    assert trace_hist == Counter({-1: 50, 2: 24, -4: 4, 5: 2, 8: 1})

    # 27 one-dimensional characters factor through K/[K,K] ~= F3^3:
    # chi_(u,v,t)(a,b,c;p)=w^(u a+v b+t p).
    one_dim = []
    for u, v, t in itertools.product(F, repeat=3):
        mult = character_inner_multiplicity(
            traces,
            lambda x, u=u, v=v, t=t:
                (u * x[0][0] + v * x[0][1] + t * x[1]) % 3,
        )
        if mult:
            one_dim.append({"label": [u, v, t], "multiplicity": mult})

    # Six 3D irreps: H27 central character s=1,2 times ext character t=0,1,2.
    # Character = 3*w^(s*c+t*p) on a=b=0 and 0 otherwise.
    three_dim = []
    for s in (1, 2):
        for t in F:
            mult = character_inner_multiplicity(
                traces,
                lambda x, s=s, t=t: (s * x[0][2] + t * x[1]) % 3,
                scalar=3,
                support_fn=lambda x: x[0][0] == 0 and x[0][1] == 0,
            )
            if mult:
                three_dim.append(
                    {
                        "central_character_exponent": s,
                        "external_character_exponent": t,
                        "multiplicity": mult,
                    }
                )

    assert one_dim == [
        {"label": [0, 0, 1], "multiplicity": 1},
        {"label": [0, 0, 2], "multiplicity": 1},
    ]
    assert three_dim == [
        {
            "central_character_exponent": 1,
            "external_character_exponent": 0,
            "multiplicity": 1,
        },
        {
            "central_character_exponent": 2,
            "external_character_exponent": 0,
            "multiplicity": 1,
        },
    ]

    dimension_check = len(one_dim) + 3 * len(three_dim)
    assert dimension_check == 8

    # Diagnostic generator traces.
    z = ((0, 0, 1), 0)
    p = ((0, 0, 0), 1)
    assert traces[KID] == 8
    assert traces[z] == -1
    assert traces[p] == 5

    parent = json.loads(
        (ROOT / "data/w33_hesse36_e8_matter81_root_lift_boundary.json").read_text()
    )
    assert parent["incidence"]["full_81x270_rank"] == 73
    assert parent["incidence"]["dark_root_dimension"] == 8

    out = {
        "schema": "w33.hesse36_e8_matter81_dark8_decomposition.v1",
        "status": "PASS_RANK73_DARK8_DECOMPOSES_AS_TWO_EXTERNAL_CHARS_PLUS_TWO_SCHRODINGER_IRREPS",
        "headline": (
            "The 8-dimensional kernel left dark by the full 81x270 cubic-incidence "
            "transform is an exact K=H27_address x C3_external subrepresentation. "
            "Its irreducible decomposition is chi_ext + chi_ext^2 + V_omega + "
            "V_omega^2, where the first two are the two nontrivial external-C3 "
            "characters and the latter two are the conjugate 3D H27 Schrodinger "
            "irreps with trivial external character. Thus the missing root-level "
            "information is representation-theoretically localized: 1+1+3+3=8."
        ),
        "incidence": {
            "shape": [81, 270],
            "rank": rank,
            "dark_dimension": 8,
            "left_K_invariant": invariant,
        },
        "dark_character": {
            "trace_histogram": {str(k): v for k, v in sorted(trace_hist.items())},
            "identity_trace": traces[KID],
            "H27_center_generator_trace": traces[z],
            "external_C3_generator_trace": traces[p],
        },
        "irreducible_decomposition": {
            "one_dimensional": one_dim,
            "three_dimensional": three_dim,
            "formula": "chi_ext + chi_ext^2 + V_omega + V_omega^2",
            "dimension_check": "1+1+3+3=8",
            "conjugation_closed": True,
        },
        "compiler_consequence": (
            "Cubic instruction amplitudes span the complementary 73-dimensional "
            "root-address subspace. Any invertible 81-root compiler must add target "
            "data carrying exactly the two nontrivial external characters and the "
            "two conjugate internal Schrodinger sectors; changing cubic signs cannot "
            "supply these sectors because nonzero row/column rephasings preserve rank."
        ),
        "boundary": (
            "The equality dark_dimension=8=rank(E8) is only numerical here. The "
            "dark module is nontrivial under K, and no identification with the E8 "
            "Cartan subalgebra is asserted."
        ),
        "parents": [
            "data/w33_hesse36_e8_matter81_root_lift_boundary.json",
            "data/w33_e8_matter81_pauli243_restriction.json",
        ],
        "checks": {
            "rank73_replayed": True,
            "dark_dimension8": True,
            "dark_space_left_K_invariant": True,
            "all_81_restricted_traces_exact": True,
            "trace_histogram_exact": True,
            "only_two_1d_irreps_present": True,
            "only_two_3d_irreps_present": True,
            "dimension_sum8": True,
            "cartan_identification_firewalled": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
