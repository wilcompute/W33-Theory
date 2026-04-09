"""Heawood branch-gap derivation of the discrete CKM amplitude.

The remaining scalar question after the discrete CKM closure was:

    why should the anchored odd-bridge strength be 7/13?

This module packages the cleanest current operator-side answer.

Already established in the repo:

1. the positive discrete CKM branch is the nonnegative spectral branch
   with common phase ``5/8``;
2. the conjugate CKM branch is the negative spectral branch
   with common phase ``3/8``;
3. the Heawood electroweak packet has exact branch weights
   ``10/13`` and ``3/13`` with gap ``7/13``.

The conservative bridge taken here is:

- pair the operator-nonnegative CKM branch with the larger Heawood weight
  ``10/13``;
- pair the operator-negative CKM branch with the smaller Heawood weight
  ``3/13``.

Then the odd-bridge strength is no longer an inserted scalar. It is the unique
branch-separation coefficient in the Heawood packet:

    10/13 - 3/13 = 7/13.

So the current exact CKM packet can be read as a branch selector on the W(3,3)
side together with the canonical Heawood branch gap on the electroweak side.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_heawood_branch_gap_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_ckm_heawood_branch_gap_summary() -> dict[str, Any]:
    ckm_branch = _load_json("w33_ckm_projector_branch_bridge_summary.json")
    ckm_packet = _load_json("w33_ckm_rank_gap_packet_bridge_summary.json")
    heawood = _load_json("w33_heawood_electroweak_polarization_bridge_summary.json")
    heawood_denominator = _load_json("w33_heawood_weinberg_denominator_bridge_summary.json")

    positive_phase = ckm_branch["best_discrete_ckm_branches"]["positive_fundamental_phase_over_pi"]
    negative_phase = ckm_branch["best_discrete_ckm_branches"]["negative_fundamental_phase_over_pi"]
    amplitude = ckm_packet["discrete_ckm_packet"]["positive_branch"]["amplitude"]

    high_weight = float(heawood["polarization_dictionary"]["hypercharge_share"]["float"])
    low_weight = float(heawood["polarization_dictionary"]["weak_share"]["float"])
    root_gap = float(heawood["polarization_dictionary"]["root_gap"]["float"])
    polarization_amplitude = float(heawood["polarization_dictionary"]["polarization_amplitude"]["float"])
    pmns23 = float(heawood_denominator["electroweak_from_heawood_dictionary"]["sin2_theta_23"]["float"])

    return {
        "status": "ok",
        "ckm_branch_dictionary": {
            "positive_branch_common_phase_over_pi": positive_phase,
            "negative_branch_common_phase_over_pi": negative_phase,
            "positive_branch_label": ckm_branch["projector_dictionary"]["nonnegative_projector"]["name"],
            "negative_branch_label": ckm_branch["projector_dictionary"]["negative_projector"]["name"],
        },
        "heawood_branch_dictionary": {
            "larger_weight": heawood["polarization_dictionary"]["hypercharge_share"],
            "smaller_weight": heawood["polarization_dictionary"]["weak_share"],
            "root_gap": heawood["polarization_dictionary"]["root_gap"],
            "polarization_amplitude": heawood["polarization_dictionary"]["polarization_amplitude"],
            "pmns23_share": heawood_denominator["electroweak_from_heawood_dictionary"]["sin2_theta_23"],
        },
        "derived_ckm_amplitude_dictionary": {
            "discrete_ckm_amplitude": {
                "exact": "7/13",
                "float": amplitude,
            },
            "heawood_branch_gap": {
                "exact": "10/13 - 3/13 = 7/13",
                "float": high_weight - low_weight,
            },
            "centered_polarization_double": {
                "exact": "2 * 7/26 = 7/13",
                "float": 2.0 * polarization_amplitude,
            },
            "pmns23_share": {
                "exact": "7/13",
                "float": pmns23,
            },
        },
        "ckm_heawood_branch_gap_theorem": {
            "positive_ckm_branch_pairs_with_larger_heawood_weight": (
                abs(positive_phase - 5.0 / 8.0) < 1e-12 and abs(high_weight - 10.0 / 13.0) < 1e-12
            ),
            "negative_ckm_branch_pairs_with_smaller_heawood_weight": (
                abs(negative_phase - 3.0 / 8.0) < 1e-12 and abs(low_weight - 3.0 / 13.0) < 1e-12
            ),
            "ckm_amplitude_equals_heawood_branch_gap": (
                abs(amplitude - (high_weight - low_weight)) < 1e-12
            ),
            "ckm_amplitude_equals_double_heawood_centered_polarization_amplitude": (
                abs(amplitude - 2.0 * polarization_amplitude) < 1e-12
            ),
            "ckm_amplitude_equals_pmns23_share": (
                abs(amplitude - pmns23) < 1e-12
            ),
        },
        "interpretive_read": (
            "Inference from the branch pairing: once the positive and negative "
            "CKM octant branches are identified with the nonnegative and "
            "negative operator branches, the only canonical scalar separating "
            "their Heawood electroweak weights is the root gap 7/13. That is "
            "also the doubled centered polarization amplitude and the PMNS23 "
            "share."
        ),
        "bridge_verdict": (
            "The odd-bridge strength is no longer best read as an inserted "
            "parameter. In the current operator dictionary, the positive CKM "
            "branch is the nonnegative branch, the conjugate branch is the "
            "negative branch, and their Heawood electroweak weights are 10/13 "
            "and 3/13. The unique branch-separation coefficient is therefore "
            "7/13, which is exactly the observed discrete CKM amplitude, the "
            "Heawood root gap, twice the centered polarization amplitude 7/26, "
            "and the PMNS23 share."
        ),
        "source_files": [
            "data/w33_ckm_projector_branch_bridge_summary.json",
            "data/w33_ckm_rank_gap_packet_bridge_summary.json",
            "data/w33_heawood_electroweak_polarization_bridge_summary.json",
            "data/w33_heawood_weinberg_denominator_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_ckm_heawood_branch_gap_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
