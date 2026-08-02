#!/usr/bin/env python3
"""Pass 2423: regular, Kantor and Ree--Tits intersection hierarchy."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGULAR = ROOT / "data" / "w33_pass2064_regular_spread_rank3_family_q357.json"
KANTOR = ROOT / "data" / "w33_pass2312_kantor_q9_symplectic_spread.json"
REE_CONTROL = ROOT / "data" / "w33_pass2203_ree_tits_nonregular_control.json"
REE_COMPLETE = ROOT / "data" / "w33_pass2300_ree_tits_divisible_code.json"
OUT = ROOT / "data" / "w33_pass2423_symplectic_spread_intersection_hierarchy.json"
EXPECTED = "TO_BE_FROZEN"


def digest(d):
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build():
    regular = json.loads(REGULAR.read_text())
    kantor = json.loads(KANTOR.read_text())
    control = json.loads(REE_CONTROL.read_text())
    ree = json.loads(REE_COMPLETE.read_text())
    assert regular["sha256_without_hash_field"] == "28c28d5078aa495c3022a6a6153b0e83d55a70a9160179c15cd23a4d8a25a60e"
    assert kantor["sha256_without_hash_field"] == "a8c878b2a98ac7592fcbb54093810ae73e8c467ebecca0d3dc8c9dfc70147eb3"
    assert control["sha256_without_hash_field"] == "7e1eaac9fec07d0dcb821855c12722177485cdc524df49f6c1448f17b30a03db"
    assert ree["sha256_without_hash_field"] == "dc6a1b4262e96210af832d098a4140f58e022bea979b7cdf3c030246dbf956e9"

    regular_rows = {}
    for qs, row in regular["complete_finite_results"].items():
        support = sorted(map(int, row["intersection_distribution"]))
        assert support == [1, int(qs) + 1]
        regular_rows[qs] = {"orbit_size": row["spreads"], "pair_intersection_support": support, "support_size": 2}

    q9_common = kantor["intersection"]["common_lines"]
    q9_fixed = kantor["intersection"]["fixed_points_of_frobenius_x3"]
    assert q9_common == 28 and len(q9_fixed) == 3

    complete = {int(k): int(v) for k, v in ree["complete_hyperplane_intersection_spectrum"].items()}
    complete_support = sorted(complete)
    regular_sections = {int(k): int(v) for k, v in ree["hyperplane_types"]["nonsquare_anisotropic_regular_sections"].items()}
    regular_section_support = sorted(regular_sections)
    closed_spread_support = sorted({int(k) for row in control["subgroup_orbits"].values() for k in row["intersection_histogram"]})
    weights = sorted(map(int, ree["projective_code"]["nonzero_weight_enumerator"]))

    checks = {
        "regular_q357_two_level": all(z["support_size"] == 2 for z in regular_rows.values()),
        "kantor_q9_mixed_pair_28": q9_common == 28,
        "kantor_value_outside_q9_regular_support": q9_common not in [1, 10],
        "kantor_fixed_subfield_mechanism": q9_common == 1 + 9 * len(q9_fixed),
        "ree_complete_support_seven_levels": complete_support == [1, 10, 19, 28, 37, 46, 55],
        "ree_regular_section_support_six_levels": regular_section_support == [10, 19, 28, 37, 46, 55],
        "ree_closed_spread_suborbit_support_five_levels": closed_spread_support == [19, 28, 37, 46, 55],
        "ree_all_sections_one_mod_9": all(x % 9 == 1 for x in complete_support),
        "ree_code_weight_gcd_9": math.gcd(*weights) == 9,
        "shared_numeric_28_has_distinct_sources": q9_common == 28 and 28 in regular_section_support,
    }
    assert all(checks.values())

    d = {
        "schema": "w33.pass2423.symplectic_spread_intersection_hierarchy.v1",
        "status": "PASS_THREE_FAMILY_HIERARCHY_WITH_DUALITY_SCOPE_EXPLICIT",
        "sources": {
            "regular_q357": {"path": str(REGULAR.relative_to(ROOT)), "sha256_without_hash_field": regular["sha256_without_hash_field"]},
            "kantor_q9": {"path": str(KANTOR.relative_to(ROOT)), "sha256_without_hash_field": kantor["sha256_without_hash_field"]},
            "ree_tits_closed_control": {"path": str(REE_CONTROL.relative_to(ROOT)), "sha256_without_hash_field": control["sha256_without_hash_field"]},
            "ree_tits_complete_hyperplanes": {"path": str(REE_COMPLETE.relative_to(ROOT)), "sha256_without_hash_field": ree["sha256_without_hash_field"]},
        },
        "regular_regular_complete_orbits": regular_rows,
        "regular_kantor_q9": {
            "common_lines": q9_common,
            "regular_support_at_q9_if_rigidity_held": [1, 10],
            "fixed_subfield_elements": q9_fixed,
            "mechanism": "x^3=x on GF(3), giving 9*3 affine common lines plus the line at infinity.",
        },
        "ree_tits_q27": {
            "closed_spread_suborbit_support": closed_spread_support,
            "regular_section_hyperplane_support": regular_section_support,
            "complete_hyperplane_support": complete_support,
            "complete_hyperplane_multiplicities": {str(k): complete[k] for k in complete_support},
            "section_ladder": "1+9j for j=0,...,6",
            "projective_code": {"parameters": ree["projective_code"]["parameters"], "nonzero_weights": weights, "weight_gcd": ree["projective_code"]["weight_gcd"]},
        },
        "coincidence_28": {
            "q9": "28=1+9*3 from the GF(3) fixed subfield in one regular/Kantor pair.",
            "q27": "28=1+9*3 is the central step j=3 of the Ree--Tits regular-section/hyperplane ladder.",
            "boundary": "The shared integer 28 does not identify the two constructions or their group orbits.",
        },
        "checks": checks,
        "theorem": "The Desarguesian regular family, the q=9 Kantor control and the q=27 Ree--Tits control exhibit three distinct intersection regimes: two-level regular/regular behavior, a fixed-subfield mixed intersection of size 28, and a multi-level 9-divisible regular-section spectrum. Hence failure of regular rigidity has more than one exact mechanism.",
        "classification_frontier": "Determine which non-Desarguesian spread families yield fixed-subfield spikes, divisible ladders, or other spectra, and which of these properties survive full automorphism orbits.",
        "boundary": "The q=9 result is one explicit mixed pair. The q=27 complete seven-level object is an ovoid-hyperplane spectrum, with regular sections identified by polar type; only the named closed suborbits are asserted as literal spread-intersection controls. No universal non-Desarguesian theorem is claimed.",
    }
    d["sha256_without_hash_field"] = digest(d)
    return d


def main():
    d = build()
    if EXPECTED != "TO_BE_FROZEN":
        assert d["sha256_without_hash_field"] == EXPECTED
        assert d == json.loads(OUT.read_text())
    print(json.dumps({"status": d["status"], "certificate": d["sha256_without_hash_field"], "regimes": 3}, sort_keys=True))


if __name__ == "__main__":
    main()
