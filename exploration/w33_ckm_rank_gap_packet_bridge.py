"""Finite rank-gap packet for the discrete CKM closure.

The recent bridges gave two exact ingredients:

1. amplitude side:
      7/13 = Heawood root gap;
2. phase side:
      5/8 (positive branch), 3/8 (conjugate branch).

This module compresses those into one finite packet law by observing that the
phase fractions are themselves normalized spectral ranks on W(3,3):

- ``5/8 = 25/40 = (1 + 24) / 40`` is the nonnegative rank share of ``E0+E1``;
- ``3/8 = 15/40`` is the negative rank share of ``E2``.

So the current discrete CKM closure can be written as

    positive branch:  (a, phi/pi) = (Phi6/Phi3, (1+24)/40),
    negative branch:  (a, phi/pi) = (Phi6/Phi3, 15/40).

In other words, the live CKM packet is already a finite root-gap times
spectral-rank-share law.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    exploration = ROOT / "exploration"
    if str(exploration) not in sys.path:
        sys.path.insert(0, str(exploration))
else:
    ROOT = Path(__file__).resolve().parents[1]
    exploration = ROOT / "exploration"
    if str(exploration) not in sys.path:
        sys.path.insert(0, str(exploration))

from w33_three_channel_operator_bridge import spectral_projector_coefficients
from w33_three_channel_operator_bridge import three_channel_entry_values


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_rank_gap_packet_bridge_summary.json"
VERTEX_COUNT = 40


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_ckm_rank_gap_packet_summary() -> dict[str, Any]:
    discrete = _load_json("w33_discrete_ckm_dictionary_bridge_summary.json")
    heawood = _load_json("w33_heawood_electroweak_polarization_bridge_summary.json")

    projector_coeffs = spectral_projector_coefficients()
    nonnegative_entries = three_channel_entry_values(projector_coeffs["E_nonnegative"])
    negative_entries = three_channel_entry_values(projector_coeffs["E2"])

    positive_candidates = [
        item for item in discrete["best_candidates"] if item["unitary_jarlskog"] > 0.0
    ]
    negative_candidates = [
        item for item in discrete["best_candidates"] if item["unitary_jarlskog"] < 0.0
    ]

    positive_phase = min(item["common_phase_over_pi"] % 1.0 for item in positive_candidates)
    negative_phase = min(item["common_phase_over_pi"] % 1.0 for item in negative_candidates)
    amplitude = float(heawood["polarization_dictionary"]["root_gap"]["float"])

    nonnegative_rank = 25
    negative_rank = 15
    nonnegative_rank_share = nonnegative_rank / VERTEX_COUNT
    negative_rank_share = negative_rank / VERTEX_COUNT

    return {
        "status": "ok",
        "heawood_root_gap": heawood["polarization_dictionary"]["root_gap"],
        "spectral_rank_dictionary": {
            "vertex_count": VERTEX_COUNT,
            "nonnegative_rank": nonnegative_rank,
            "negative_rank": negative_rank,
            "nonnegative_rank_share": {
                "exact": "25/40 = 5/8",
                "float": nonnegative_rank_share,
            },
            "negative_rank_share": {
                "exact": "15/40 = 3/8",
                "float": negative_rank_share,
            },
        },
        "projector_diagonal_dictionary": {
            "nonnegative_projector_diagonal": nonnegative_entries["diagonal"],
            "negative_projector_diagonal": negative_entries["diagonal"],
        },
        "discrete_ckm_packet": {
            "positive_branch": {
                "amplitude": amplitude,
                "amplitude_exact": "7/13",
                "common_phase_over_pi": positive_phase,
                "common_phase_exact": "5/8",
                "physical_theta_over_pi": 2.0 * positive_phase,
                "physical_theta_exact": "5/4",
            },
            "negative_branch": {
                "amplitude": amplitude,
                "amplitude_exact": "7/13",
                "common_phase_over_pi": negative_phase,
                "common_phase_exact": "3/8",
                "physical_theta_over_pi": 2.0 * negative_phase,
                "physical_theta_exact": "3/4",
            },
        },
        "ckm_rank_gap_packet_theorem": {
            "positive_common_phase_equals_nonnegative_rank_share": (
                abs(positive_phase - nonnegative_rank_share) < 1e-12
                and nonnegative_entries["diagonal"] == "5/8"
            ),
            "negative_common_phase_equals_negative_rank_share": (
                abs(negative_phase - negative_rank_share) < 1e-12
                and negative_entries["diagonal"] == "3/8"
            ),
            "best_discrete_ckm_amplitude_equals_heawood_root_gap": (
                abs(amplitude - 7.0 / 13.0) < 1e-12
            ),
            "positive_ckm_packet_equals_root_gap_times_nonnegative_rank_share": (
                abs(amplitude - 7.0 / 13.0) < 1e-12
                and abs(positive_phase - 25.0 / 40.0) < 1e-12
            ),
            "conjugate_ckm_packet_equals_root_gap_times_negative_rank_share": (
                abs(amplitude - 7.0 / 13.0) < 1e-12
                and abs(negative_phase - 15.0 / 40.0) < 1e-12
            ),
        },
        "interpretive_read": (
            "Inference from the exact packet match: the live CKM target no "
            "longer looks like an arbitrary rational fit. It is a finite packet "
            "built from one Heawood gap ratio and one normalized spectral rank "
            "share of W(3,3)."
        ),
        "bridge_verdict": (
            "The discrete CKM closure now compresses to one finite law. The "
            "amplitude is the Heawood root gap 7/13, while the common phase is "
            "the normalized spectral rank share of the chosen branch: 25/40 = "
            "5/8 for the positive nonnegative branch, and 15/40 = 3/8 for the "
            "conjugate negative branch. So the current exact CKM packet is a "
            "root-gap times rank-share object."
        ),
        "source_files": [
            "data/w33_discrete_ckm_dictionary_bridge_summary.json",
            "data/w33_heawood_electroweak_polarization_bridge_summary.json",
            "exploration/w33_three_channel_operator_bridge.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_ckm_rank_gap_packet_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
