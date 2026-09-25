#!/usr/bin/env python3
"""Pass 10948: clock-tetracode negacyclic / reciprocal-factor hyperbolic bridge.

This pass starts from the exact Pass 10946 oriented P1(F3) evaluation
tetracode and asks a different question: can its four clock coordinates be
put into a genuine negacyclic polynomial gauge without changing the code?

The answer is yes, but only after an orientation lift.  Two single-coordinate
sign flips give the two reciprocal principal ideals of F3[x]/(x^4+1).
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from w33_affine_tetracode_e8_glue_bridge import (
    STANDARD_TETRACODE_GENERATORS,
    span,
)

P = 3
OUT = ROOT / "data/w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge.json"


def mod(x: int) -> int:
    return int(x) % P


def code_span(basis):
    return frozenset(
        tuple(mod(a * basis[0][j] + b * basis[1][j]) for j in range(4))
        for a, b in itertools.product(range(P), repeat=2)
    )


def negashift(v):
    """Multiplication by x in F3[x]/(x^4+1), coefficient order c0..c3."""
    return (mod(-v[3]), v[0], v[1], v[2])


def n_power(v, n):
    out = tuple(v)
    for _ in range(n):
        out = negashift(out)
    return out


def sign_gauge(code, signs):
    return frozenset(
        tuple(mod(signs[j] * w[j]) for j in range(4))
        for w in code
    )


def perm_sign_gauge(code, perm, signs):
    return frozenset(
        tuple(mod(signs[j] * w[perm[j]]) for j in range(4))
        for w in code
    )


def invariant_under_negashift(code):
    return all(negashift(w) in code for w in code)


def dot(u, v):
    return mod(sum(a * b for a, b in zip(u, v)))


def conv(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = mod(out[i + j] + x * y)
    return tuple(out)


def reciprocal_conjugation(v):
    """p(x) -> p(x^-1) in R, using x^-1=-x^3 because x^4=-1."""
    return (v[0], mod(-v[3]), mod(-v[2]), mod(-v[1]))


def matrix_rank_mod3(rows):
    a = [list(map(mod, row)) for row in rows]
    r = 0
    if not a:
        return 0
    for c in range(len(a[0])):
        piv = next((i for i in range(r, len(a)) if a[i][c]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        inv = pow(a[r][c], -1, P)
        a[r] = [mod(inv * x) for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [mod(x - q * y) for x, y in zip(a[i], a[r])]
        r += 1
    return r


def main():
    repo_code = frozenset(span(STANDARD_TETRACODE_GENERATORS))
    assert len(repo_code) == 9

    # Pass 10946's frozen orientation is deliberately not the standard
    # negacyclic gauge.
    assert not invariant_under_negashift(repo_code)

    # Coefficient convention: -1 is represented by 2 in F3.
    f_plus = (2, 1, 1)   # x^2 + x - 1
    f_minus = (2, 2, 1)  # x^2 - x - 1
    assert conv(f_plus, f_minus) == (1, 0, 0, 0, 1)

    g_plus = f_plus + (0,)
    g_minus = f_minus + (0,)
    ideal_plus = code_span((g_plus, negashift(g_plus)))
    ideal_minus = code_span((g_minus, negashift(g_minus)))

    # Two one-ray orientation flips take the exact Pass 10946 clock code to
    # the two reciprocal negacyclic ideals.
    gauge_plus = (1, 2, 1, 1)
    gauge_minus = (1, 1, 1, 2)
    clock_plus = sign_gauge(repo_code, gauge_plus)
    clock_minus = sign_gauge(repo_code, gauge_minus)
    assert clock_plus == ideal_plus
    assert clock_minus == ideal_minus
    assert invariant_under_negashift(clock_plus)
    assert invariant_under_negashift(clock_minus)

    # The negacyclic clock has exact order 8: N^4=-I, N^8=I.
    for code in (clock_plus, clock_minus):
        for w in code:
            assert n_power(w, 4) == tuple(mod(-x) for x in w)
            assert n_power(w, 8) == w
    probe = next(w for w in clock_plus if any(w))
    assert all(n_power(probe, n) != probe for n in range(1, 8))

    # Each ideal is a totally isotropic/self-dual [4,2,3]_3 tetracode.
    for code in (clock_plus, clock_minus):
        assert all(dot(u, v) == 0 for u in code for v in code)
        assert matrix_rank_mod3(list(code)) == 2
        weights = {sum(x != 0 for x in w) for w in code if any(w)}
        assert weights == {3}

    # They are transverse and the cross pairing is perfect.
    assert clock_plus.intersection(clock_minus) == {(0, 0, 0, 0)}
    b_plus = (g_plus, negashift(g_plus))
    b_minus = (g_minus, negashift(g_minus))
    cross = tuple(tuple(dot(u, v) for v in b_minus) for u in b_plus)
    assert cross == ((1, 1), (2, 1))
    cross_det = mod(cross[0][0] * cross[1][1] - cross[0][1] * cross[1][0])
    assert cross_det == 2

    # Cyclotomic inversion exchanges the reciprocal ideals.
    assert {reciprocal_conjugation(w) for w in clock_plus} == set(clock_minus)
    assert {reciprocal_conjugation(w) for w in clock_minus} == set(clock_plus)

    # Signed-permutation orbit census.  B4 has order 4!*2^4=384; the
    # tetracode monomial stabilizer has order 48, hence eight code images.
    orbit = {}
    negacyclic_gauges = []
    for perm in itertools.permutations(range(4)):
        for signs in itertools.product((1, 2), repeat=4):
            image = perm_sign_gauge(repo_code, perm, signs)
            key = tuple(sorted(image))
            orbit.setdefault(key, 0)
            orbit[key] += 1
            if invariant_under_negashift(image):
                negacyclic_gauges.append((perm, signs, key))
    assert len(orbit) == 8
    assert set(orbit.values()) == {48}
    negacyclic_images = {x[2] for x in negacyclic_gauges}
    assert len(negacyclic_images) == 2
    assert len(negacyclic_gauges) == 96

    # Existing repo anchors: same Phi_8 reciprocal factor pair in the
    # Pass 9961-9984 split branch, and the already frozen E8 tetracode glue.
    unitary = json.loads(
        (ROOT / "data/PART_W33_PASS9961_9984_THE_UNITARY_BRANCH.json").read_text()
    )
    witness = unitary["trichotomy"]["third_branch_verified_at"]["polynomial_witness"]
    assert "x^2+x-1" in witness and "x^2-x-1" in witness
    assert "reciprocal" in witness

    glue = json.loads(
        (ROOT / "manuscripts/parts/PART_MCCCLXXXVII_AFFINE_TETRACODE_E8_GLUE_BRIDGE_results.json").read_text()
    )
    assert glue["checks"]["representative_matches_standard_tetracode"] is True
    assert glue["e8_glue_count"]["identity"] == "240 = 4*6 + 8*27"

    out = {
        "schema": "w33.pass10948.clock_tetracode_negacyclic_hyperbolic_bridge.v1",
        "status": "PASS_CLOCK_TETRACODE_NEGACYCLIC_HYPERBOLIC_BRIDGE",
        "frozen_clock_code": {
            "generators": [list(x) for x in STANDARD_TETRACODE_GENERATORS],
            "negacyclic_in_frozen_orientation": False,
        },
        "phi8_factorization_mod3": {
            "identity": "x^4+1=(x^2+x-1)(x^2-x-1) over F3",
            "factor_plus": "x^2+x-1",
            "factor_minus": "x^2-x-1",
            "factors_are_reciprocal": True,
        },
        "orientation_gauges": {
            "plus": {
                "coordinate_signs": list(gauge_plus),
                "meaning": "flip the second oriented P1(F3) clock representative",
                "ideal": "(x^2+x-1) in F3[x]/(x^4+1)",
            },
            "minus": {
                "coordinate_signs": list(gauge_minus),
                "meaning": "flip the fourth oriented P1(F3) clock representative",
                "ideal": "(x^2-x-1) in F3[x]/(x^4+1)",
            },
        },
        "negacyclic_clock": {
            "shift": "N(c0,c1,c2,c3)=(-c3,c0,c1,c2)",
            "N4": "-I",
            "N8": "I",
            "operator_order": 8,
            "factor_minimal_polynomials": ["x^2+x-1", "x^2-x-1"],
            "each_sector_dimension_F3": 2,
            "each_sector_reading": "one-dimensional over F9 after choosing a root of its irreducible quadratic",
        },
        "hyperbolic_pair": {
            "plus_is_totally_isotropic": True,
            "minus_is_totally_isotropic": True,
            "each_is_self_dual_tetracode": True,
            "intersection_dimension": 0,
            "ambient_direct_sum_dimension": 4,
            "cross_pairing_matrix_in_polynomial_bases": [list(r) for r in cross],
            "cross_pairing_determinant_mod3": cross_det,
            "cross_pairing_nondegenerate": True,
            "cyclotomic_inversion": "p(x)->p(x^-1), x^-1=-x^3",
            "cyclotomic_inversion_swaps_sectors": True,
        },
        "monomial_orbit": {
            "signed_permutation_group_order": 384,
            "distinct_tetracode_images": len(orbit),
            "stabilizer_order": 48,
            "distinct_negacyclic_images": len(negacyclic_images),
            "signed_permutation_gauges_yielding_negacyclicity": len(negacyclic_gauges),
            "gauges_per_negacyclic_image": 48,
        },
        "repo_welds": {
            "pass10946": "the source code is the exact oriented P1(F3) clock evaluation tetracode",
            "pass9961_9984": "the same reciprocal Phi_8 factors define the verified d=8,l=3 split branch",
            "existing_E8_glue": glue["e8_glue_count"]["identity"],
            "new_objectwise_reading": (
                "the clock tetracode is a rank-one F9 hyperbolic-pair shadow of the same "
                "reciprocal-prime Phi_8 mechanism used by the later cyclotomic branch"
            ),
        },
        "theorem": (
            "The exact Pass 10946 clock tetracode has two and only two distinct standard "
            "negacyclic images in its signed-permutation orbit. They are the principal "
            "ideals generated by the reciprocal irreducible factors x^2+x-1 and x^2-x-1 "
            "of Phi_8=x^4+1 over F3. Each image is a self-dual [4,2,3]_3 tetracode on "
            "which the negacyclic shift has order eight; the two images intersect only "
            "at zero, pair nondegenerately with one another, and are exchanged by "
            "cyclotomic inversion. Thus the four-ray clock code and the repo's Pass "
            "9961-9984 reciprocal-prime split are the same finite algebraic mechanism "
            "at different module ranks, not merely the same factor count."
        ),
        "boundary": (
            "Negacyclicity is an algebraic clock/code gauge, not a physical arrow of time. "
            "The comparison to Pass 9961-9984 is a shared Phi_8 reciprocal-factor and "
            "hyperbolic-pair mechanism; it does not identify the two carriers as the same "
            "representation, nor does it promote the finite clock to continuum time."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "orbit_images": len(orbit),
        "negacyclic_images": len(negacyclic_images),
        "negacyclic_gauges": len(negacyclic_gauges),
        "cross_det": cross_det,
    }, indent=2))


if __name__ == "__main__":
    main()
