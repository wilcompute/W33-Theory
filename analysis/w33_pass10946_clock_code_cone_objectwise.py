#!/usr/bin/env python3
"""Pass 10946: clock-code-cone objectwise theorem.

The four points of P1(F3) are simultaneously used as oriented evaluation
coordinates for the repository tetracode and, after projectivization and the
symmetric-square Veronese map, as the four frozen temporal null directions.
The sign choice of a projective representative is retained explicitly.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from w33_affine_tetracode_e8_glue_bridge import (
    STANDARD_TETRACODE_GENERATORS,
    span,
)

OUT = ROOT / "data/w33_pass10946_clock_code_cone_objectwise.json"
P = 3

# These representatives make evaluation exactly equal to the repository's
# frozen standard tetracode, not merely monomially equivalent to it.
ORIENTED_REPS = ((1, 0), (0, 1), (1, 1), (2, 1))
NORMALIZED_REPS = ((1, 0), (0, 1), (1, 1), (1, 2))
def mod(x):
    return int(x) % P


def det2(g):
    return mod(g[0][0]*g[1][1] - g[0][1]*g[1][0])


def inv2(g):
    d = det2(g)
    assert d
    di = pow(d, -1, P)
    return (
        (mod(di*g[1][1]), mod(-di*g[0][1])),
        (mod(-di*g[1][0]), mod(di*g[0][0])),
    )


def matvec(g, v):
    return (
        mod(g[0][0]*v[0] + g[0][1]*v[1]),
        mod(g[1][0]*v[0] + g[1][1]*v[1]),
    )


def projective(v):
    x, y = map(mod, v)
    assert (x, y) != (0, 0)
    s = pow(x if x else y, -1, P)
    return (mod(s*x), mod(s*y))
def eval_word(form):
    a, b = map(mod, form)
    return tuple(mod(a*x + b*y) for x, y in ORIENTED_REPS)


def sym2(v):
    x, y = map(mod, v)
    return (mod(x*x), mod(x*y), mod(y*y))


def qsym(s):
    a, b, c = map(mod, s)
    return mod(a*c - b*b)


def oriented_match(v):
    """Return (coordinate, scalar) with v=scalar*ORIENTED_REPS[coordinate]."""
    pv = projective(v)
    k = next(i for i, r in enumerate(ORIENTED_REPS) if projective(r) == pv)
    r = ORIENTED_REPS[k]
    for scalar in (1, 2):
        if tuple(mod(scalar*z) for z in r) == tuple(map(mod, v)):
            return k, scalar
    raise AssertionError((v, k))


def monomial_pullback(g):
    """Action on evaluations of l o g^{-1}."""
    gi = inv2(g)
    perm = []
    scales = []
    for r in ORIENTED_REPS:
        k, mu = oriented_match(matvec(gi, r))
        perm.append(k)
        scales.append(mu)
    return tuple(perm), tuple(scales)
def apply_monomial(word, perm, scales):
    return tuple(mod(scales[j]*word[perm[j]]) for j in range(4))


def main():
    repo_code = span(STANDARD_TETRACODE_GENERATORS)
    eval_code = {eval_word((a, b)) for a, b in itertools.product(range(3), repeat=2)}
    assert eval_code == repo_code
    assert len(eval_code) == 9
    weights = Counter(sum(x != 0 for x in w) for w in eval_code)
    assert weights == Counter({3: 8, 0: 1})

    # The fourth repo representative is -1 times the conventional normalized
    # representative [1:-1].  That projective sign is exactly what changes
    # a-b to b-a and matches the frozen tetracode convention.
    lift_rows = []
    for j, (o, n) in enumerate(zip(ORIENTED_REPS, NORMALIZED_REPS)):
        assert projective(o) == projective(n)
        scalar = next(s for s in (1, 2)
                      if tuple(mod(s*x) for x in n) == o)
        lift_rows.append({
            "coordinate": j,
            "oriented_rep": list(o),
            "normalized_projective_rep": list(n),
            "orientation_scalar": scalar,
        })
    assert [r["orientation_scalar"] for r in lift_rows] == [1, 1, 1, 2]

    # Every nonzero clock form omits exactly one projective clock point.
    clock_pairs = []
    nonzero_forms = [(a, b) for a, b in itertools.product(range(3), repeat=2)
                     if (a, b) != (0, 0)]
    used = set()
    for j in range(4):
        forms = [f for f in nonzero_forms if eval_word(f)[j] == 0]
        assert len(forms) == 2
        words = [eval_word(f) for f in forms]
        assert words[1] == tuple(mod(-x) for x in words[0])
        assert all(sum(x != 0 for x in w) == 3 for w in words)
        used.update(forms)
        clock_pairs.append({
            "clock_coordinate": j,
            "projective_ray": list(NORMALIZED_REPS[j]),
            "oriented_forms": [list(f) for f in forms],
            "oriented_codewords": [list(w) for w in words],
        })
    assert len(used) == 8

    m36 = json.loads((ROOT / "data/w33_20260924_m36_null_line_atlas.json").read_text())
    family_rows = m36["M36_coordinates"]["family_records"]
    family_by_p1 = {tuple(r["P1_direction"]): r for r in family_rows}
    assert set(family_by_p1) == set(NORMALIZED_REPS)
    objectwise = []
    for j, rep in enumerate(NORMALIZED_REPS):
        null = sym2(rep)
        assert qsym(null) == 0
        fr = family_by_p1[rep]
        assert tuple(fr["null_direction"]) == null
        objectwise.append({
            "tetracode_coordinate": j,
            "oriented_clock_rep": list(ORIENTED_REPS[j]),
            "projective_clock_ray": list(rep),
            "symmetric_square_null_ray": list(null),
            "M36_family": fr["family_name"],
            "M36_family_index": fr["family"],
            "Hesse_parallel_class": fr["Hesse_parallel_class"],
            "bell_line_point": fr["bell_line_point"],
        })
    assert [r["M36_family"] for r in objectwise] == ["B", "A", "C", "D"]

    null_parent = json.loads(
        (ROOT / "data/w33_hesse_nullcone_adjoint_intertwiner.json").read_text()
    )
    assert null_parent["checks"]["veronese_dictionary_exact"] is True
    assert null_parent["checks"]["GL2_image_S4_order24"] is True
    GL2 = []
    monomial_actions = {}
    point_perms = Counter()
    for entries in itertools.product(range(3), repeat=4):
        g = ((entries[0], entries[1]), (entries[2], entries[3]))
        if not det2(g):
            continue
        GL2.append(g)
        perm, scales = monomial_pullback(g)
        assert {apply_monomial(w, perm, scales) for w in eval_code} == eval_code
        monomial_actions[(perm, scales)] = g
        point_perms[perm] += 1
    assert len(GL2) == 48
    assert len(monomial_actions) == 48
    assert len(point_perms) == 24
    assert set(point_perms.values()) == {2}

    for g in GL2:
        ng = tuple(tuple(mod(-x) for x in row) for row in g)
        p1, s1 = monomial_pullback(g)
        p2, s2 = monomial_pullback(ng)
        assert p1 == p2
        assert s2 == tuple(mod(-x) for x in s1)
    calibrations = [
        (j, orientation, origin)
        for j in range(4) for orientation in (1, 2) for origin in range(3)
    ]
    assert len(calibrations) == 24

    glue = json.loads(
        (ROOT / "manuscripts/parts/PART_MCCCLXXXVII_AFFINE_TETRACODE_E8_GLUE_BRIDGE_results.json").read_text()
    )
    assert glue["checks"]["representative_matches_standard_tetracode"] is True
    assert glue["e8_glue_count"]["identity"] == "240 = 4*6 + 8*27"

    out = {
        "schema": "w33.pass10946.clock_code_cone_objectwise.v1",
        "status": "PASS_CLOCK_CODE_CONE_OBJECTWISE_THEOREM",
        "clock_line": {
            "space": "P1(F3)",
            "projective_rays": [list(x) for x in NORMALIZED_REPS],
            "oriented_evaluation_representatives": [list(x) for x in ORIENTED_REPS],
            "orientation_lifts": lift_rows,
        },
        "tetracode": {
            "evaluation_rule": "ell_(a,b)(x,y)=a*x+b*y",
            "evaluation_formula": "(a,b,a+b,2a+b)=(a,b,a+b,b-a)",
            "repo_generators": [list(x) for x in STANDARD_TETRACODE_GENERATORS],
            "evaluation_code_equals_repo_standard_exactly": True,
            "size": len(eval_code),
            "weight_enumerator": {"0": weights[0], "3": weights[3]},
            "four_opposite_pairs_by_omitted_clock": clock_pairs,
        },
        "cone_dictionary": {
            "symmetric_square": "nu(x,y)=(x^2,x*y,y^2)",
            "quadratic_form": "q(a,b,c)=a*c-b^2",
            "all_four_images_null": True,
            "coordinate_to_existing_geometry": objectwise,
            "M36_family_order_in_tetracode_coordinates": ["B", "A", "C", "D"],
            "matches_existing_M36_Hesse_null_atlas_objectwise": True,
        },
        "symmetry": {
            "GL2_order": len(GL2),
            "distinct_monomial_tetracode_actions": len(monomial_actions),
            "projective_permutation_image_order": len(point_perms),
            "projective_image": "PGL(2,3) ~= S4",
            "kernel_on_projective_rays": "{+I,-I}",
            "same_projective_permutation_has_two_global_sign_lifts": True,
            "complete_clock_calibrations": len(calibrations),
            "calibration_count": "4 frames * 2 orientations * 3 origins = 24",
        },
        "E8_glue_crosscheck": {
            "existing_standard_tetracode_certificate": glue["part"],
            "existing_root_identity": glue["e8_glue_count"]["identity"],
            "new_reading": (
                "the four A2 glue coordinates are the four projective clock rays; "
                "the eight nonzero glue words are the two oriented linear clock "
                "functions vanishing at each of the four rays"
            ),
        },
        "theorem": (
            "With oriented projective representatives (1,0),(0,1),(1,1),(2,1), "
            "evaluation of all linear forms on P1(F3) is exactly the repository's "
            "frozen ternary tetracode, including its fourth-coordinate sign convention. "
            "Projectivizing those representatives and applying the symmetric-square "
            "Veronese map gives, coordinate by coordinate, the four null directions "
            "already attached to M36 families B,A,C,D, their Hesse striations and Bell "
            "points. GL(2,3) acts by 48 exact monomial tetracode automorphisms; modulo "
            "the global sign lift it induces the same order-24 PGL(2,3)=S4 action on "
            "the four clock rays. Thus the code-coordinate sign is not arbitrary: it "
            "is an oriented lift of the projective clock/null direction."
        ),
        "boundary": (
            "This is finite F3 projective geometry plus a code and null-cone theorem. "
            "The orientation scalar is an algebraic sign lift. A thermodynamic arrow "
            "still requires open-system irreversibility; the theorem does not promote "
            "the finite determinant cone to continuum Lorentz spacetime."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "families": out["cone_dictionary"]["M36_family_order_in_tetracode_coordinates"],
        "actions": len(monomial_actions),
        "projective_S4": len(point_perms),
        "calibrations": len(calibrations),
    }, indent=2))


if __name__ == "__main__":
    main()
