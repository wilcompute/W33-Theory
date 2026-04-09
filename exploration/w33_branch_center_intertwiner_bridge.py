"""Centered intertwiner between the CKM branch packet and the Heawood packet.

The recent CKM closure reduced to a two-branch packet:

    CKM branch packet      = diag(5/8, 3/8)
    Heawood weight packet  = diag(10/13, 3/13)

Both packets are centered at ``1/2``. Their only nontrivial content is the
coefficient of the same branch involution ``sigma = diag(1,-1)``:

    diag(5/8, 3/8)   = 1/2 I + 1/8 sigma
    diag(10/13, 3/13)= 1/2 I + 7/26 sigma

So there is a unique centered intertwiner preserving the branch involution:

    W_heawood - 1/2 I = ((28/13)) (W_ckm - 1/2 I)

and the scale factor is itself native to the repo:

    28/13 = 4 Phi_6 / Phi_3 = (q^3 + 1) / Phi_3.

This turns the branch pairing from an interpretation into a rigid centered
two-state law. The CKM positive/negative branches and the Heawood
larger/smaller weights are the same branch involution seen at two different
polarization strengths.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_branch_center_intertwiner_bridge_summary.json"
Q = 3
PHI3 = 13
PHI6 = 7


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_branch_center_intertwiner_summary() -> dict[str, Any]:
    ckm_rank_gap = _load_json("w33_ckm_rank_gap_packet_bridge_summary.json")
    heawood = _load_json("w33_heawood_electroweak_polarization_bridge_summary.json")

    ckm_positive = ckm_rank_gap["discrete_ckm_packet"]["positive_branch"]["common_phase_over_pi"]
    ckm_negative = ckm_rank_gap["discrete_ckm_packet"]["negative_branch"]["common_phase_over_pi"]
    heawood_high = float(heawood["polarization_dictionary"]["hypercharge_share"]["float"])
    heawood_low = float(heawood["polarization_dictionary"]["weak_share"]["float"])

    ckm_packet = np.diag([ckm_positive, ckm_negative])
    heawood_packet = np.diag([heawood_high, heawood_low])
    identity = np.eye(2, dtype=float)
    sigma = np.diag([1.0, -1.0])

    ckm_centered = ckm_packet - 0.5 * identity
    heawood_centered = heawood_packet - 0.5 * identity
    ckm_strength = float(ckm_centered[0, 0])
    heawood_strength = float(heawood_centered[0, 0])
    scale = heawood_strength / ckm_strength

    return {
        "status": "ok",
        "ckm_branch_packet": {
            "matrix": [[float(value) for value in row] for row in ckm_packet.tolist()],
            "formula": "diag(5/8, 3/8) = 1/2 I + 1/8 sigma",
            "centered_strength": {
                "exact": "1/8",
                "float": ckm_strength,
            },
        },
        "heawood_weight_packet": {
            "matrix": [[float(value) for value in row] for row in heawood_packet.tolist()],
            "formula": "diag(10/13, 3/13) = 1/2 I + 7/26 sigma",
            "centered_strength": {
                "exact": "7/26",
                "float": heawood_strength,
            },
        },
        "centered_intertwiner_dictionary": {
            "branch_involution": "sigma = diag(1,-1)",
            "intertwiner_scale": {
                "exact": "28/13 = 4 Phi_6 / Phi_3 = (q^3 + 1) / Phi_3",
                "float": scale,
            },
            "scaled_ckm_centered_packet": [
                [float(value) for value in row]
                for row in (scale * ckm_centered).tolist()
            ],
            "heawood_centered_packet": [
                [float(value) for value in row]
                for row in heawood_centered.tolist()
            ],
        },
        "branch_center_intertwiner_theorem": {
            "ckm_packet_is_centered_one_half_plus_one_eighth_branch_involution": (
                np.allclose(ckm_packet, 0.5 * identity + 0.125 * sigma)
            ),
            "heawood_packet_is_centered_one_half_plus_seven_over_twentysix_branch_involution": (
                np.allclose(heawood_packet, 0.5 * identity + (7.0 / 26.0) * sigma)
            ),
            "same_branch_involution_controls_both_packets": (
                np.allclose(ckm_centered, ckm_strength * sigma)
                and np.allclose(heawood_centered, heawood_strength * sigma)
            ),
            "heawood_centered_packet_is_native_scale_multiple_of_ckm_centered_packet": (
                np.allclose(heawood_centered, scale * ckm_centered)
            ),
            "intertwiner_scale_equals_28_over_13_equals_4phi6_over_phi3_equals_q_cubed_plus_1_over_phi3": (
                abs(scale - 28.0 / 13.0) < 1e-12
                and abs(scale - (4.0 * PHI6) / PHI3) < 1e-12
                and abs(scale - (Q**3 + 1.0) / PHI3) < 1e-12
            ),
        },
        "interpretive_read": (
            "Inference from the centered packets: the CKM branch shares and the "
            "Heawood electroweak weights are not merely analogous ratios. They "
            "are the same two-state branch involution with different centered "
            "polarization strengths, related by one native q=3 cyclotomic scale."
        ),
        "bridge_verdict": (
            "The branch pairing is now rigid at the two-state level. The CKM "
            "packet is 1/2 I + 1/8 sigma, the Heawood packet is "
            "1/2 I + 7/26 sigma, and the unique centered intertwiner between "
            "them has scale 28/13 = 4 Phi_6 / Phi_3 = (q^3+1)/Phi_3. So the "
            "positive and negative CKM branches are not being matched to the "
            "Heawood weights by hand; both sides are the same branch involution "
            "seen at two exact polarization scales."
        ),
        "source_files": [
            "data/w33_ckm_rank_gap_packet_bridge_summary.json",
            "data/w33_heawood_electroweak_polarization_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_branch_center_intertwiner_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
