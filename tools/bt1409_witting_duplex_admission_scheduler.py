#!/usr/bin/env python3
"""BT1409: split Witting communication into state and basis admission laws.

BT1408 proved the state-compatibility shell for a Witting communication round:

    1 same + 12 compatible + 27 incompatible = 40, so accepts at 13/40.

BT1409 adds the second layer that the architecture needs.  A selected Witting
ray lives in exactly four tetrads.  Therefore the basis/witness aperture is

    4 accepted bases / 40 bases = 1/10.

Terminology firewall (2026-09-09): 1/10 is the exact Kochen--Specker
satisfiability defect / witness-aperture rate.  It is NOT the
Abramsky--Barbosa contextual fraction.  The latter is 1 for the strongly
contextual W(3,3) empirical model because there is no global section/ovoid.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,
    find_tetrads,
    load_json,
    memberships,
)

OUT = ROOT / "data" / "bt1409_witting_duplex_admission_scheduler.json"


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def classify_for_ray(
    ray: int,
    tetrads: list[tuple[int, int, int, int]],
    ray_to_bases: list[list[int]],
) -> dict[str, Any]:
    witness_bases = sorted(ray_to_bases[ray])
    compatible_multiset: list[int] = []
    basis_rows = []
    for basis_id, tetrad in enumerate(tetrads):
        contains = ray in tetrad
        if contains:
            compatible_multiset.extend(tetrad)
        basis_rows.append(
            {
                "basis_id": basis_id,
                "tetrad": list(tetrad),
                "mode": "WITNESS_APERTURE" if contains else "RETRY_SHADOW",
            }
        )

    compatible_unique = sorted(set(compatible_multiset))
    compatible_distinct = [
        candidate for candidate in compatible_unique if candidate != ray
    ]
    return {
        "ray": ray,
        "witness_bases": witness_bases,
        "basis_accept_count": len(witness_bases),
        "basis_reject_count": len(tetrads) - len(witness_bases),
        "basis_accept_rate": fraction_text(Fraction(len(witness_bases), len(tetrads))),
        "basis_reject_rate": fraction_text(
            Fraction(len(tetrads) - len(witness_bases), len(tetrads))
        ),
        "compatible_state_unique_count": len(compatible_unique),
        "compatible_distinct_count": len(compatible_distinct),
        "incompatible_state_count": 40 - len(compatible_unique),
        "state_accept_rate": fraction_text(Fraction(len(compatible_unique), 40)),
        "state_reject_rate": fraction_text(Fraction(40 - len(compatible_unique), 40)),
        "compatible_incidence_count": len(compatible_multiset),
        "compatible_incidence_rate": fraction_text(
            Fraction(len(compatible_multiset), len(tetrads) * 4)
        ),
        "same_ray_incidence_multiplicity": compatible_multiset.count(ray),
        "compatible_unique": compatible_unique,
        "compatible_distinct": compatible_distinct,
        "basis_epoch": basis_rows,
    }


def build_result() -> dict[str, Any]:
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    ray_to_bases, _pair_to_bases = memberships(tetrads)

    bt823 = load_json("data/bt823_the_closure.json")
    pass1080 = load_json("data/w33_pass1080_contextual_fraction_audit.json")
    bt1407 = load_json("data/bt1407_microframe_transaction_composer.json")
    bt1408 = load_json("data/bt1408_witting_contextual_communication_bridge.json")

    ray_profiles = [classify_for_ray(ray, tetrads, ray_to_bases) for ray in range(40)]
    sample = ray_profiles[0]

    histograms = {
        "basis_accept_count": Counter(
            row["basis_accept_count"] for row in ray_profiles
        ),
        "basis_reject_count": Counter(
            row["basis_reject_count"] for row in ray_profiles
        ),
        "compatible_state_unique_count": Counter(
            row["compatible_state_unique_count"] for row in ray_profiles
        ),
        "compatible_distinct_count": Counter(
            row["compatible_distinct_count"] for row in ray_profiles
        ),
        "incompatible_state_count": Counter(
            row["incompatible_state_count"] for row in ray_profiles
        ),
        "compatible_incidence_count": Counter(
            row["compatible_incidence_count"] for row in ray_profiles
        ),
    }
    histograms_json = {
        name: {str(key): value for key, value in sorted(hist.items())}
        for name, hist in histograms.items()
    }

    frame_ticks = 72
    communication_frames = sample["compatible_state_unique_count"]
    basis_witness_frames = sample["basis_accept_count"]
    checks = {
        "bt1408_bridge_verified": bt1408["verified"] is True,
        "bt1408_uses_precise_contextuality_labels": (
            bt1408["contextuality_budget"]["ks_satisfiability_defect"] == "1/10"
            and bt1408["contextuality_budget"]["abramsky_barbosa_contextual_fraction"] == 1
            and "contextual_fraction" not in bt1408["contextuality_budget"]
        ),
        "bt823_contextual_budget_loaded": bt823["ks_exact_max"] == 36
        and bt823["contextual_deficit"] == 4,
        "pass1080_contextual_fraction_is_one": (
            pass1080["contextual_fraction"]["W33"]["value"] == 1.0
            and pass1080["contextual_fraction"]["W33"]["ovoids"] == 0
        ),
        "bt1407_frame_loaded": bt1407["verified"] is True
        and bt1407["frame_identity"]
        == "48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks",
        "every_ray_has_four_witness_bases": histograms_json["basis_accept_count"]
        == {"4": 40},
        "basis_reject_count_matches_bt823_ks_max": histograms_json["basis_reject_count"]
        == {"36": 40},
        "basis_aperture_rate_is_ks_defect": {
            row["basis_accept_rate"] for row in ray_profiles
        }
        == {"1/10"},
        "state_accept_rate_is_bt1408_key_rate": {
            row["state_accept_rate"] for row in ray_profiles
        }
        == {"13/40"},
        "state_reject_shell_is_matter_27": histograms_json["incompatible_state_count"]
        == {"27": 40},
        "incidence_accept_rate_matches_ks_defect": {
            row["compatible_incidence_rate"] for row in ray_profiles
        }
        == {"1/10"},
        "same_ray_has_four_basis_multiplicity": {
            row["same_ray_incidence_multiplicity"] for row in ray_profiles
        }
        == {4},
    }

    return {
        "bt": 1409,
        "title": "Witting duplex admission scheduler",
        "verified": all(checks.values()),
        "duplex_law": {
            "state_query": (
                "unique compatible states accept at 13/40 = "
                "1 same + 12 orthogonal over 40 rays"
            ),
            "basis_query": (
                "witness bases accept at 4/40 = 1/10, equal to the exact "
                "KS satisfiability defect"
            ),
            "basis_shadow": (
                "the 36/40 rejected basis choices match the corrected BT823 "
                "best approximately satisfiable context count"
            ),
        },
        "contextuality_quantities": {
            "ks_satisfiability_defect": "1/10",
            "abramsky_barbosa_contextual_fraction": 1,
            "why_distinct": (
                "The KS defect asks how close a Boolean marking can come to "
                "satisfying all exactly-one context constraints (36/40). The "
                "Abramsky-Barbosa contextual fraction is 1 because no global "
                "section exists at all."
            ),
        },
        "histograms": histograms_json,
        "rates": {
            "state_accept_unique": "13/40",
            "state_reject_unique": "27/40",
            "basis_witness_aperture": "1/10",
            "basis_retry_shadow": "36/40",
            "incidence_accept": "1/10",
        },
        "frame_budget_for_one_selected_ray": {
            "communication_frames": communication_frames,
            "basis_witness_frames": basis_witness_frames,
            "frame_ticks": frame_ticks,
            "communication_ticks_if_all_compatible_states_are_served": (
                communication_frames * frame_ticks
            ),
            "basis_witness_ticks_if_all_apertures_are_audited": (
                basis_witness_frames * frame_ticks
            ),
            "reading": (
                "BT1409 does not require every rejected choice to consume a "
                "BT1407 frame.  It separates the accepted communication frames "
                "from the smaller basis-witness aperture used for contextual "
                "tamper evidence."
            ),
        },
        "sample_ray_0": sample,
        "architecture_breakthrough": (
            "The Witting protocol has two different acceptance clocks.  The "
            "state clock admits 13/40 compatible communication partners.  The "
            "basis clock admits 4/40 witness apertures, numerically equal to the "
            "exact KS satisfiability defect 1/10.  The Abramsky-Barbosa contextual "
            "fraction is a different quantity and equals 1."
        ),
        "boundary": (
            "BT1409 is a finite scheduler/count certificate.  It does not prove "
            "cryptographic security, channel loss tolerance, or physical detector "
            "calibration.  The basis aperture / KS defect must not be relabeled "
            "as the Abramsky-Barbosa contextual fraction."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "basis_witness_aperture": result["rates"]["basis_witness_aperture"],
                "state_accept_unique": result["rates"]["state_accept_unique"],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
