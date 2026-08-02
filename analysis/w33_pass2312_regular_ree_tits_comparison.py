#!/usr/bin/env python3
"""Pass 2312: exact regular-vs-Ree--Tits spread comparison.

The regular q=3,5,7 family and the exhaustive q=27 Ree--Tits spectrum already
exist independently.  This pass places them in one invariant ledger and extracts
the precise statement that survives: two-intersection rank-three behavior is a
regular/Desarguesian fingerprint, whereas the Ree--Tits control has a seven-level
9-divisible spectrum.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from functools import reduce
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGULAR = ROOT / "data" / "w33_pass2064_regular_spread_rank3_family_q357.json"
CONTROL = ROOT / "data" / "w33_pass2203_ree_tits_nonregular_control.json"
REE = ROOT / "data" / "w33_pass2300_ree_tits_divisible_code.json"


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-json", type=Path)
    args = ap.parse_args()

    regular = json.loads(REGULAR.read_text())
    control = json.loads(CONTROL.read_text())
    ree = json.loads(REE.read_text())

    q = 27
    regular_predicted = [1, q + 1]
    spectrum = {int(k): int(v) for k, v in ree["complete_hyperplane_intersection_spectrum"].items()}
    support = sorted(spectrum)
    expected_support = [1 + 9 * j for j in range(7)]
    weights = sorted(q * q + 1 - z for z in support)
    weight_gcd = reduce(gcd, weights)
    suborbit_support = sorted({int(k) for row in control["subgroup_orbits"].values() for k in row["intersection_histogram"]})

    checks = {
        "regular_q27_prediction_is_1_28": regular_predicted == [1, 28],
        "ree_tits_support_is_full_1_plus_9j_ladder": support == expected_support,
        "all_ree_tits_sections_one_mod_9": all(z % 9 == 1 for z in support),
        "not_all_sections_one_mod_27": any(z % 27 != 1 for z in support),
        "projective_code_exactly_9_divisible": weight_gcd == 9,
        "closed_144_suborbit_uses_nonregular_values": any(z not in regular_predicted for z in suborbit_support),
        "control_and_complete_spectrum_agree": set(suborbit_support).issubset(support),
        "hyperplane_count_complete": sum(spectrum.values()) == ree["projective_hyperplanes"],
    }
    assert all(checks.values())

    regular_cases = {}
    for qs, row in regular["complete_finite_results"].items():
        vals = sorted(int(k) for k in row["intersection_distribution"])
        assert vals == [1, int(qs) + 1]
        regular_cases[qs] = {
            "spreads": row["spreads"],
            "intersection_support": vals,
            "support_size": len(vals),
        }

    out = {
        "schema": "w33.pass2312.regular_ree_tits_comparison.v1",
        "status": "PASS_REGULAR_TWO_LEVEL_VS_REE_TITS_SEVEN_LEVEL_SEPARATION",
        "regular_complete_cases": regular_cases,
        "regular_q27_formula_prediction": regular_predicted,
        "ree_tits_q27_complete_support": support,
        "ree_tits_q27_multiplicities": {str(k): spectrum[k] for k in support},
        "ree_tits_section_ladder": "1+9j for j=0,...,6",
        "ree_tits_projective_code_weights": weights,
        "ree_tits_weight_gcd": weight_gcd,
        "closed_suborbit_support": suborbit_support,
        "checks": checks,
        "theorem": "The regular-spread family has two intersection levels {1,q+1} in every complete tested case q=3,5,7, while the exhaustive q=27 Ree--Tits control has seven levels 1,10,19,28,37,46,55 and an exactly 9-divisible [730,5]_27 projective code. Therefore the two-level rank-three scheme is not a universal symplectic-spread law.",
        "new_fingerprint": "At q=27, regular behavior would occupy only the endpoints 1 and 28 of the first four positions, whereas Ree--Tits fills the entire seven-step 9-adic section ladder. Divisibility, rather than two-intersection regularity, is the surviving exceptional invariant.",
        "boundary": "This comparison distinguishes the specified Ree--Tits ovoid from the regular family. It does not classify all non-Desarguesian symplectic spreads or assert universal 9-divisibility.",
    }
    out["sha256_without_hash_field"] = digest(out)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
