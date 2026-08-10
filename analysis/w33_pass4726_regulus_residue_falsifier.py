#!/usr/bin/env python3
"""Pass 4726 companion falsifier: the new 270 residues are not the BT794 regulus-transversal sets.

BT794 associates to each of the 540 skew W33 line pairs its four common
isotropic transversals.  Passes 4721--4725 produce 270 four-line residue masks.
Both families consist of four pairwise-skew W33 lines, so equality is a tempting
count/shape guess.  This script tests it exactly and rejects it.

Result:
  * BT794 gives 540 distinct four-transversal sets;
  * the residue shell gives 270 distinct four-line sets;
  * the two families are disjoint;
  * every residue meets the 540 transversal sets with profile
        |R cap T| = 0^360, 1^144, 2^36,
    hence never in 3 or 4 lines;
  * dually every transversal set sees residue profile
        |R cap T| = 0^180, 1^72, 2^18.

This is a boundary theorem, not a bridge: the involution residues are special
four-line partial spreads, but not the existing BT794 regulus-transversal
carrier.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4725_4726_involution_residue_dual_code import residue_shell

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4726_REGULUS_RESIDUE_FALSIFIER.json"


def main() -> int:
    _pts, _pidx, lines, astar, apartments, _apmasks, _H = geometry()
    residues = residue_shell(lines, apartments)
    assert len(residues) == 270

    trans_masks = []
    for a, b in itertools.combinations(range(40), 2):
        if astar[a, b]:
            continue
        trans = [k for k in range(40) if k not in (a, b) and astar[k, a] and astar[k, b]]
        assert len(trans) == 4
        assert all(not astar[i, j] for i, j in itertools.combinations(trans, 2))
        trans_masks.append(sum(1 << k for k in trans))
    assert len(trans_masks) == 540
    assert len(set(trans_masks)) == 540

    R = set(residues)
    T = set(trans_masks)
    assert R.isdisjoint(T)

    pair_profile = Counter((r & t).bit_count() for r in residues for t in trans_masks)
    assert pair_profile == Counter({0: 97200, 1: 38880, 2: 9720})

    residue_profiles = Counter(
        tuple(sorted(Counter((r & t).bit_count() for t in trans_masks).items()))
        for r in residues
    )
    transversal_profiles = Counter(
        tuple(sorted(Counter((r & t).bit_count() for r in residues).items()))
        for t in trans_masks
    )
    expected_r = ((0, 360), (1, 144), (2, 36))
    expected_t = ((0, 180), (1, 72), (2, 18))
    assert residue_profiles == Counter({expected_r: 270})
    assert transversal_profiles == Counter({expected_t: 540})

    out = {
        "pass": 4726,
        "kind": "companion falsifier",
        "BT794_skew_charts": 540,
        "distinct_BT794_transversal_sets": 540,
        "involution_residues": 270,
        "family_intersection_size": 0,
        "global_pair_intersection_profile": {str(k): v for k, v in sorted(pair_profile.items())},
        "per_residue_profile_against_540_transversal_sets": {"0": 360, "1": 144, "2": 36},
        "per_transversal_profile_against_270_residues": {"0": 180, "1": 72, "2": 18},
        "maximum_cross_intersection": 2,
        "falsified_claim": "the 270 involution residues are BT794 four-transversal regulus sets",
        "boundary": "Both are four-line pairwise-skew W33 objects, but they are disjoint families with uniform cross-intersection at most two. The residue shell must not be identified with the BT794 regulus-transversal carrier by shape or cardinality.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
