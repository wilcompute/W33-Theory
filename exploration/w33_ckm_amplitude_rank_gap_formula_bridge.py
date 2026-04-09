"""Exact rank-gap formula for the discrete CKM amplitude.

The centered branch-intertwiner bridge identified two exact internal factors:

1. a spectral branch-gap on the W(3,3) side
      5/8 - 3/8 = 10/40 = Theta(W33) / v;
2. a centered Heawood scaling factor
      28/13 = (q^3 + 1) / Phi_3 = 4 Phi_6 / Phi_3.

This module packages the key consequence:

    ((q^3 + 1) / Phi_3) * (Theta(W33) / v)
      = (28/13) * (10/40)
      = 7/13.

So the live CKM amplitude is no longer just a Heawood branch gap or an inserted
dictionary value. It is exactly

    a_CKM = topological_scale * spectral_rank_gap.

That is the cleanest current scalar law in the repo.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_amplitude_rank_gap_formula_bridge_summary.json"
Q = 3
PHI3 = 13
THETA_W33 = 10
VERTEX_COUNT = 40


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_ckm_amplitude_rank_gap_formula_summary() -> dict[str, Any]:
    ckm_rank_gap = _load_json("w33_ckm_rank_gap_packet_bridge_summary.json")
    centered = _load_json("w33_branch_center_intertwiner_bridge_summary.json")

    positive_phase = ckm_rank_gap["discrete_ckm_packet"]["positive_branch"]["common_phase_over_pi"]
    negative_phase = ckm_rank_gap["discrete_ckm_packet"]["negative_branch"]["common_phase_over_pi"]
    amplitude = ckm_rank_gap["discrete_ckm_packet"]["positive_branch"]["amplitude"]
    branch_gap = positive_phase - negative_phase
    rank_gap = 25 - 15
    rank_gap_share = rank_gap / VERTEX_COUNT
    topological_scale = float(centered["centered_intertwiner_dictionary"]["intertwiner_scale"]["float"])

    return {
        "status": "ok",
        "ckm_branch_gap_dictionary": {
            "positive_phase_share": {
                "exact": "5/8",
                "float": positive_phase,
            },
            "negative_phase_share": {
                "exact": "3/8",
                "float": negative_phase,
            },
            "branch_gap": {
                "exact": "5/8 - 3/8 = 1/4",
                "float": branch_gap,
            },
            "rank_gap": {
                "exact": "25 - 15 = 10 = Theta(W33)",
                "float": float(rank_gap),
            },
            "rank_gap_share": {
                "exact": "10/40 = Theta(W33)/v = 1/4",
                "float": rank_gap_share,
            },
        },
        "topological_scale_dictionary": {
            "intertwiner_scale": centered["centered_intertwiner_dictionary"]["intertwiner_scale"],
            "q_cubed_plus_one": {
                "exact": "q^3 + 1 = 28",
                "float": float(Q**3 + 1),
            },
            "phi3": {
                "exact": "Phi_3 = 13",
                "float": float(PHI3),
            },
            "theta_w33": {
                "exact": "Theta(W33) = 10",
                "float": float(THETA_W33),
            },
            "vertex_count": {
                "exact": "v = 40",
                "float": float(VERTEX_COUNT),
            },
        },
        "derived_ckm_amplitude_formula": {
            "discrete_ckm_amplitude": {
                "exact": "7/13",
                "float": amplitude,
            },
            "topological_scale_times_branch_gap": {
                "exact": "((q^3+1)/Phi_3) * (1/4) = (28/13) * (1/4) = 7/13",
                "float": topological_scale * branch_gap,
            },
            "topological_scale_times_rank_gap_share": {
                "exact": "((q^3+1)/Phi_3) * (Theta(W33)/v) = (28/13) * (10/40) = 7/13",
                "float": topological_scale * rank_gap_share,
            },
        },
        "ckm_amplitude_rank_gap_formula_theorem": {
            "branch_gap_equals_theta_over_v": (
                abs(branch_gap - THETA_W33 / VERTEX_COUNT) < 1e-12
            ),
            "topological_scale_equals_q_cubed_plus_one_over_phi3": (
                abs(topological_scale - (Q**3 + 1) / PHI3) < 1e-12
            ),
            "ckm_amplitude_equals_topological_scale_times_branch_gap": (
                abs(amplitude - topological_scale * branch_gap) < 1e-12
            ),
            "ckm_amplitude_equals_topological_scale_times_theta_over_v": (
                abs(amplitude - topological_scale * THETA_W33 / VERTEX_COUNT) < 1e-12
            ),
            "ckm_amplitude_equals_7_over_13": (
                abs(amplitude - 7.0 / 13.0) < 1e-12
            ),
        },
        "interpretive_read": (
            "Inference from the exact factorization: the CKM amplitude is built "
            "from two purely internal finite ingredients. The W(3,3) side "
            "provides the branch gap Theta/v = 1/4, while the Heawood-side "
            "centered intertwiner contributes the topological scale "
            "(q^3+1)/Phi_3 = 28/13."
        ),
        "bridge_verdict": (
            "The scalar closure is now explicit. The discrete CKM amplitude "
            "satisfies a_CKM = ((q^3+1)/Phi_3) * (Theta(W33)/v) exactly, i.e. "
            "a_CKM = (28/13) * (10/40) = 7/13. So the live CKM packet is not "
            "just a branch label plus an inserted amplitude. Its amplitude is "
            "an exact topological-scale times spectral-rank-gap law."
        ),
        "source_files": [
            "data/w33_branch_center_intertwiner_bridge_summary.json",
            "data/w33_ckm_rank_gap_packet_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_ckm_amplitude_rank_gap_formula_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
