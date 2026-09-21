#!/usr/bin/env python3
"""Classify the two certified E8 order-six actions by affine Kac coordinates.

The repository currently has two distinct inner order-six E8 actions:
  (A) the structural FI x matter-parity Z6, with adjoint eigendimensions
      (54,48,33,32,33,48);
  (B) the flagship physical/holonomy C6, with adjoint eigendimensions
      (44,40,38,48,38,40).

Kac's classification of inner finite-order automorphisms says that an exact
order-m class is represented by nonnegative relatively-prime affine labels
(s0,...,s8) satisfying sum_i a_i s_i=m, where a_i are the affine highest-root
marks.  This verifier exhausts every normalized order-six Kac diagram of E8,
computes its root-space eigendimensions, and identifies both repository
actions uniquely.

It also computes the fixed root systems of g, g^2, and g^3.  This gives a
standard Lie-theoretic explanation for the already-certified fact that the
two Z6 actions are distinct but have Weyl-conjugate D8 cubes.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import math
import sys
from collections import Counter
from functools import reduce
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_e8_order6_kac_classification.json"

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

TARGET_EDGES = {
    "A2": (2, [(0, 1)]),
    "A3": (3, [(0, 1), (1, 2)]),
    "D4": (4, [(0, 1), (1, 2), (1, 3)]),
    "D5": (5, [(0, 1), (1, 2), (2, 3), (2, 4)]),
    "E6": (6, [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)]),
    "D7": (7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]),
    "D8": (8, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7)]),
}

def classify_root_subsystem(old, roots, h):
    simp = old.simple_roots(roots, h)
    A = old.cartan(simp)
    comps = old.components_from_cartan(A)
    types = []
    for C in comps:
        hits = []
        for name, (n, edges) in TARGET_EDGES.items():
            if len(C) == n and old.graph_isomorphic_component(A, C, edges):
                hits.append(name)
        assert len(hits) == 1, (len(C), C, hits)
        types.append(hits[0])
    return "+".join(sorted(types)), len(simp)

def gcd_all(xs):
    return reduce(math.gcd, xs)

def main(write=True):
    old = load(
        ROOT / "analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py",
        "w33_kac_parent",
    )
    structural = json.loads(
        (ROOT / "data/w33_physical_fi_matter_parity_z6_quotient.json").read_text()
    )
    holonomy = json.loads(
        (ROOT / "data/w33_physical_holonomy_e8_chevalley_lift.json").read_text()
    )

    roots = old.e8_roots_doubled()
    h = (1, 3, 9, 27, 81, 243, 729, 2187)
    simp = old.simple_roots(roots, h)
    cm = old.coeff_map(roots, simp)
    pos = [r for r in roots if old.dot(r, h) > 0]
    highest = max(pos, key=lambda r: sum(cm[r]))
    marks = tuple(cm[highest])
    assert marks == (4, 6, 5, 4, 3, 2, 2, 3)
    affine_marks = (1,) + marks

    target_structural = tuple(structural["Z6"]["dimensions"])
    target_holonomy = tuple(holonomy["physical_C6_eigenvalue_multiplicities"])
    assert target_structural == (54, 48, 33, 32, 33, 48)
    assert target_holonomy == (44, 40, 38, 48, 38, 40)

    def dims(s):
        finite = s[1:]
        cnt = Counter(
            sum(c * a for c, a in zip(cm[r], finite)) % 6 for r in roots
        )
        cnt[0] += 8
        return tuple(cnt[k] for k in range(6))

    candidates = []
    ranges = [range(6 // a + 1) for a in affine_marks]
    for s in itertools.product(*ranges):
        if sum(a * x for a, x in zip(affine_marks, s)) != 6:
            continue
        if gcd_all(s) != 1:
            continue
        candidates.append((s, dims(s)))
    assert len(candidates) == 20

    hits_structural = [s for s, d in candidates if d == target_structural]
    hits_holonomy = [s for s, d in candidates if d == target_holonomy]
    assert hits_structural == [(2, 0, 0, 0, 1, 0, 0, 0, 0)]
    assert hits_holonomy == [(0, 0, 0, 0, 1, 0, 0, 1, 0)]

    S = hits_structural[0]
    H = hits_holonomy[0]
    # Both diagrams use the same mark-4 finite node.  The remaining Kac weight
    # two sits on the affine node for the structural class and on a mark-2
    # finite node for the holonomy class.
    assert affine_marks[4] == 4 and affine_marks[7] == 2
    assert sum(a * x for a, x in zip(affine_marks, S)) == 6
    assert sum(a * x for a, x in zip(affine_marks, H)) == 6

    def power_ladder(s):
        finite = s[1:]
        ans = {}
        for p in (1, 2, 3):
            fixed_roots = [
                r
                for r in roots
                if p * sum(c * a for c, a in zip(cm[r], finite)) % 6 == 0
            ]
            typ, rank = classify_root_subsystem(old, fixed_roots, h)
            ans[str(p)] = {
                "root_count": len(fixed_roots),
                "semisimple_type": typ,
                "semisimple_rank": rank,
                "center_rank": 8 - rank,
                "fixed_lie_dimension": len(fixed_roots) + 8,
            }
        return ans

    ladder_S = power_ladder(S)
    ladder_H = power_ladder(H)
    assert ladder_S["1"] == {
        "root_count": 46,
        "semisimple_type": "A2+D5",
        "semisimple_rank": 7,
        "center_rank": 1,
        "fixed_lie_dimension": 54,
    }
    assert ladder_S["2"] == {
        "root_count": 78,
        "semisimple_type": "A2+E6",
        "semisimple_rank": 8,
        "center_rank": 0,
        "fixed_lie_dimension": 86,
    }
    assert ladder_S["3"] == {
        "root_count": 112,
        "semisimple_type": "D8",
        "semisimple_rank": 8,
        "center_rank": 0,
        "fixed_lie_dimension": 120,
    }
    assert ladder_H["1"] == {
        "root_count": 36,
        "semisimple_type": "A3+D4",
        "semisimple_rank": 7,
        "center_rank": 1,
        "fixed_lie_dimension": 44,
    }
    assert ladder_H["2"] == {
        "root_count": 84,
        "semisimple_type": "D7",
        "semisimple_rank": 7,
        "center_rank": 1,
        "fixed_lie_dimension": 92,
    }
    assert ladder_H["3"] == ladder_S["3"]

    out = {
        "schema": "w33.e8_order6_kac_classification.v1",
        "status": "PASS_UNIQUE_TWIN_ORDER6_E8_KAC_CLASSES_AND_POWER_LADDERS",
        "affine_highest_root_marks_repo_order": list(affine_marks),
        "normalized_exact_order6_kac_diagrams_enumerated": len(candidates),
        "structural_FI_x_matter_parity_Z6": {
            "eigendimensions": list(target_structural),
            "unique_kac_coordinates": list(S),
            "weighted_order": sum(a * x for a, x in zip(affine_marks, S)),
            "power_ladder": ladder_S,
        },
        "flagship_holonomy_Z6": {
            "eigendimensions": list(target_holonomy),
            "unique_kac_coordinates": list(H),
            "weighted_order": sum(a * x for a, x in zip(affine_marks, H)),
            "power_ladder": ladder_H,
        },
        "shared_cube": {
            "power": 3,
            "fixed_type": "D8",
            "fixed_dimension": 120,
            "interpretation": "the two order-six classes have conjugate matter-parity/D8 involution cubes",
        },
        "separation": {
            "same_order6_class": False,
            "structural_fixed": "D5+A2+u1",
            "holonomy_fixed": "D4+A3+u1",
            "structural_square_fixed": "E6+A2",
            "holonomy_square_fixed": "D7+u1",
            "kac_difference": "the remaining Kac weight 2 is affine (s0=2) for FI x parity, but finite mark-2 (s7=1) for the holonomy class",
        },
        "candidate_table": [
            {"kac": list(s), "eigendimensions": list(d)} for s, d in candidates
        ],
        "literature_anchor": "Kac/Cartan classification of inner torsion automorphisms by affine Kac coordinates; see M. Reeder, Enseign. Math. 56 (2010), 3-47, Secs. 2.2 and 2.4.",
        "boundary": "This is an exact conjugacy-class classification inside complex E8. It does not by itself prove a heterotic vacuum preserves matter parity or identify either order-six class with spacetime/orbifold dynamics beyond the separately certified physical inputs.",
        "checks": {
            "twenty_order6_inner_kac_classes": True,
            "structural_spectrum_selects_unique_class": True,
            "holonomy_spectrum_selects_unique_class": True,
            "structural_square_is_E6_A2": True,
            "holonomy_square_is_D7_u1": True,
            "both_cubes_are_D8": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main(True)
