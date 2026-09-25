#!/usr/bin/env python3
"""Exact E6-cubic bracket ladder for the E8 node-7 temporal grading.

The positive nilpotent algebra is modeled as
  g1 = V(27) x U(2), g2 = V*(27), g3 = U(2),
with [x⊗u,y⊗v] = eps(u,v) (x cross y) and
[x⊗u,z*] = <x,z*> u.

The repo's canonical signed 45-term E6 cubic supplies the cross product.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260925_cubic_clock_bracket_ladder.json"
CUBIC = ROOT / "artifacts/canonical_su3_gauge_and_cubic.json"
WELD = ROOT / "data/w33_e6_cubic_diagonal_phase_weld.json"
GRADING = ROOT / "data/w33_20260925_hesse_clock_e8_gradings.json"

EPS = np.array([[0, 1], [-1, 0]], dtype=int)


def load_signed_triads():
    payload = json.loads(CUBIC.read_text())
    rows = payload["solution"]["d_triples"]
    triads = {tuple(r["triple"]): int(r["sign"]) for r in rows}
    assert len(triads) == 45
    return triads
def pair_cross_table(triads):
    table = {}
    pair_mult = Counter()
    var_mult = Counter()
    for tri, sign in triads.items():
        i, j, k = tri
        for a, b, c in ((i, j, k), (i, k, j), (j, k, i)):
            key = tuple(sorted((a, b)))
            pair_mult[key] += 1
            assert key not in table
            table[key] = (c, sign)
        for x in tri:
            var_mult[x] += 1
    assert set(pair_mult.values()) == {1}
    assert len(table) == 135
    assert len(var_mult) == 27 and set(var_mult.values()) == {5}
    return table, var_mult


def cross_basis(i, j, table):
    if i == j:
        return None
    return table.get(tuple(sorted((i, j))))


def cubic_basis(i, j, k, triads):
    return triads.get(tuple(sorted((i, j, k))), 0)


def grade1_bracket(i, a, j, b, table):
    e = int(EPS[a, b])
    if e == 0:
        return None
    z = cross_basis(i, j, table)
    if z is None:
        return None
    k, sign = z
    return (k, e * sign)


def grade12_bracket(i, a, k, coeff=1):
    # [e_i tensor u_a, z^k] = delta_i^k u_a.
    if i != k:
        return None
    return (a, int(coeff))
def nested_left(i, a, j, b, k, c, table):
    # [[i,a],[j,b]] first lands in g2; [g2,g1] is minus [g1,g2].
    z = grade1_bracket(i, a, j, b, table)
    if z is None:
        return np.zeros(2, dtype=int)
    dual, coeff = z
    if dual != k:
        return np.zeros(2, dtype=int)
    out = np.zeros(2, dtype=int)
    out[c] = -coeff
    return out


def main():
    triads = load_signed_triads()
    table, var_mult = pair_cross_table(triads)

    # Pairwise g1 brackets span all 27 g2 basis directions exactly.
    outputs = set()
    nonzero_pairs = 0
    same_orientation_nonzero = 0
    opposite_orientation_nonzero = 0
    for i, a, j, b in itertools.product(range(27), range(2), range(27), range(2)):
        z = grade1_bracket(i, a, j, b, table)
        if z is None:
            continue
        nonzero_pairs += 1
        outputs.add(z[0])
        if a == b:
            same_orientation_nonzero += 1
        else:
            opposite_orientation_nonzero += 1
    assert outputs == set(range(27))
    assert same_orientation_nonzero == 0
    assert opposite_orientation_nonzero > 0

    # The next bracket spans both top-clock directions.
    top_outputs = {
        grade12_bracket(i, a, i)[0]
        for i in range(27) for a in range(2)
    }
    assert top_outputs == {0, 1}
    # Jacobi on all cubic-supported basis triples and all 2^3 orientations.
    jacobi_checks = 0
    triple_tick_checks = 0
    for tri, sign in triads.items():
        i, j, k = tri
        for a, b, c in itertools.product(range(2), repeat=3):
            J = (
                nested_left(i, a, j, b, k, c, table)
                + nested_left(j, b, k, c, i, a, table)
                + nested_left(k, c, i, a, j, b, table)
            )
            assert np.array_equal(J, np.zeros(2, dtype=int))
            jacobi_checks += 1

            # The first nested term is exactly -eps(a,b) N(e_i,e_j,e_k) u_c.
            lhs = nested_left(i, a, j, b, k, c, table)
            rhs = np.zeros(2, dtype=int)
            rhs[c] = -int(EPS[a, b]) * sign
            assert np.array_equal(lhs, rhs)
            triple_tick_checks += 1

    # Pure one-ray temporal controls are abelian at grade one.
    for ray in (0, 1):
        for i, j in itertools.product(range(27), repeat=2):
            assert grade1_bracket(i, ray, j, ray, table) is None

    # Full temporal doublet has exact growth 54 -> 81 -> 83.
    growth = [54, 54 + len(outputs), 54 + len(outputs) + len(top_outputs)]
    assert growth == [54, 81, 83]

    grading = json.loads(GRADING.read_text())
    weld = json.loads(WELD.read_text())
    assert grading["oriented_three_tick_grading"]["positive_nilpotent_growth"] == growth
    assert weld["weld_consequence"]["required_retyped_dimension"] == 54
    assert weld["weld_consequence"]["diagonal_center_external_weld_covers_full_retyped_quotient"]
    out = {
        "schema": "w33.20260925.cubic_clock_bracket_ladder.v1",
        "status": "PASS_SIGNED_E6_CUBIC_GENERATES_EXACT_54_81_83_CLOCK_LADDER",
        "canonical_cubic": {
            "source": "artifacts/canonical_su3_gauge_and_cubic.json",
            "signed_triads": len(triads),
            "sign_distribution": dict(Counter(triads.values())),
            "variable_count": len(var_mult),
            "triads_per_variable": sorted(set(var_mult.values())),
            "pair_to_third_coordinate_entries": len(table),
            "pair_support_is_simple": True,
        },
        "graded_model": {
            "g1": "27 tensor 2",
            "dim_g1": 54,
            "g2": "dual 27",
            "dim_g2": len(outputs),
            "g3": "temporal doublet 2",
            "dim_g3": len(top_outputs),
            "positive_nilpotent_dimension": growth[-1],
            "growth_vector": growth,
            "bracket_11": "[x⊗u,y⊗v]=eps(u,v)(x cross y)",
            "bracket_12": "[x⊗u,z*]=<x,z*>u",
            "same_temporal_ray_bracket_is_zero": True,
            "two_temporal_rays_generate_all_g2": True,
            "g1_g2_generates_both_g3_directions": True,
        },
        "cubic_tick": {
            "jacobi_basis_checks": jacobi_checks,
            "nested_cubic_checks": triple_tick_checks,
            "identity": (
                "[[X⊗u,Y⊗v],W⊗w] = -eps(u,v) N(X,Y,W) w "
                "for the declared bracket convention"
            ),
            "interpretation": (
                "Three grade-one updates can create a top-grade clock displacement "
                "exactly when the polarized E6 cubic is nonzero and the first two "
                "temporal directions are linearly independent."
            ),
        },
        "repo_crosscheck": {
            "Hesse_clock_grading_status": grading["status"],
            "phase_weld_status": weld["status"],
            "phase_weld_retyped_dimension": 54,
            "diagonal_weld_projection_rank": weld["rank_and_alignment"][
                "center_plus_external"
            ]["quotient_projection_rank"],
            "pure_center_projection_rank": weld["rank_and_alignment"]["center"][
                "quotient_projection_rank"
            ],
            "pure_external_projection_rank": weld["rank_and_alignment"]["external"][
                "quotient_projection_rank"
            ],
        },
        "theorem": (
            "Using the repository's canonical signed 45-term E6 cubic, the symmetric "
            "cross product of the 27-dimensional carrier spans all 27 dual directions. "
            "Tensoring the carrier with a two-dimensional temporal space and contracting "
            "with its alternating form makes same-ray grade-one controls commute, while "
            "opposite temporal rays generate the full 27-dimensional grade-two layer. "
            "The natural evaluation bracket with grade two then generates both dimensions "
            "of grade three. The resulting positive algebra has exact growth 54->81->83, "
            "and the nested bracket is the signed polarized E6 cubic times the remaining "
            "temporal vector. Basis Jacobi holds because eps(u,v)w+eps(v,w)u+eps(w,u)v=0 "
            "in dimension two."
        ),
        "boundary": (
            "This proves the abstract node-7 E8 nilpotent bracket ladder on the repo's "
            "signed E6 cubic carrier and exactly matches the Hesse-clock grading counts. "
            "The existing diagonal phase weld independently surjects onto a 54-dimensional "
            "quotient, but this packet does not yet construct the 54x54 intertwiner proving "
            "that quotient is literally this 27 tensor 2 grade-one module. That is now the "
            "sharp remaining identification."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "growth": growth,
        "g2_outputs": len(outputs),
        "g3_outputs": len(top_outputs),
        "jacobi_checks": jacobi_checks,
        "cubic_checks": triple_tick_checks,
    }, indent=2))


if __name__ == "__main__":
    main()
