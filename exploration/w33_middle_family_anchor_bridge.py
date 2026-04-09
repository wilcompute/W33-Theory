"""Middle-family anchor theorem on the quark-bearing side.

The recent selector-side work showed that the actual ``3U`` packet carries
three exact heavy/light seesaw pairs with very different imbalance ratios.
Independently, the diffuse Higgs quark packet came back with family sign vector
``(-,+,-)``, and the older block-level CKM scan already had a best candidate
whose middle family decouples while the outer pair mixes.

This module packages the exact overlap of those three facts. The same family is
singled out by all of them:

- it is the unique least-split / most balanced selector family;
- it is the unique positive entry in the diffuse quark family parity;
- it is the exact fixed family in the best legacy block CKM candidate; and
- it is the shared block anchor in the best vertex-level quark scan.

So the current quark-bearing story is no longer "three generic families".
It is a middle-family anchor with an outer-pair mixing shell.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_middle_family_anchor_bridge_summary.json"
TOL = 1e-10
FAMILY_ORDER = ("U1", "U2", "U3")


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _balance_selector(heavy: float, light: float) -> float:
    return 4.0 * heavy * light / (heavy + light) ** 2


@lru_cache(maxsize=1)
def build_middle_family_anchor_summary() -> dict[str, Any]:
    seesaw = _load_json("w33_three_family_seesaw_bridge_summary.json")
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")

    family_pairs = seesaw["family_pairs"]
    balance_selectors = {
        family: _balance_selector(report["heavy_scale"], report["light_scale"])
        for family, report in family_pairs.items()
    }
    balance_descending = sorted(balance_selectors, key=balance_selectors.get, reverse=True)
    most_balanced_family = balance_descending[0]

    heavy_descending = seesaw["orderings"]["heavy_descending"]
    light_descending = seesaw["orderings"]["light_descending"]

    h1_family_sign = [int(value) for value in signs["h1_family_sign_vector"]]
    hbar1_family_sign = [int(value) for value in signs["hbar1_family_sign_vector"]]
    singled_family_indices = [index for index, value in enumerate(h1_family_sign) if value > 0]
    if len(singled_family_indices) != 1:
        raise AssertionError("expected one distinguished positive family in the diffuse sign packet")
    singled_family_index = singled_family_indices[0]
    singled_family_label = FAMILY_ORDER[singled_family_index]

    parity = np.diag(h1_family_sign).astype(float)
    best_block_v = np.array(blocks["best_block"]["V_CKM"], dtype=float)
    best_vertex = blocks["vertex_scan_best"]
    best_vertex_v = np.array(best_vertex["V_CKM"], dtype=float)

    middle_projector = np.zeros((3, 3), dtype=float)
    middle_projector[singled_family_index, singled_family_index] = 1.0
    outer_projector = np.eye(3, dtype=float) - middle_projector

    commutator = best_block_v @ parity - parity @ best_block_v
    vertex_commutator = best_vertex_v @ parity - parity @ best_vertex_v
    outer_middle_coupling = (
        np.linalg.norm(outer_projector @ best_block_v @ middle_projector)
        + np.linalg.norm(middle_projector @ best_block_v @ outer_projector)
    )
    outer_pair_matrix = (
        outer_projector @ best_block_v @ outer_projector
    )[np.ix_([index for index in range(3) if index != singled_family_index],
             [index for index in range(3) if index != singled_family_index])]

    return {
        "status": "ok",
        "family_balance_selectors": balance_selectors,
        "balance_ordering_descending": balance_descending,
        "diffuse_quark_family_parity": {
            "h1": h1_family_sign,
            "hbar1": hbar1_family_sign,
            "singled_family_index_zero_based": singled_family_index,
            "singled_family_label": singled_family_label,
        },
        "best_legacy_block_candidate": {
            "matrix": [[float(value) for value in row] for row in best_block_v.tolist()],
            "parity_commutator_norm": float(np.linalg.norm(commutator)),
            "outer_middle_coupling_norm": float(outer_middle_coupling),
            "middle_diagonal_entry": float(
                (middle_projector @ best_block_v @ middle_projector)[
                    singled_family_index, singled_family_index
                ]
            ),
            "outer_pair_submatrix": [[float(value) for value in row] for row in outer_pair_matrix.tolist()],
        },
        "best_vertex_scan_anchor": {
            "up_block_zero_based": int(best_vertex["v_up_block"]),
            "down_block_zero_based": int(best_vertex["v_dn_block"]),
            "shared_family_label": FAMILY_ORDER[int(best_vertex["v_up_block"])],
            "ckm_error": float(best_vertex["ckm_error"]),
            "parity_commutator_norm": float(np.linalg.norm(vertex_commutator)),
        },
        "middle_family_anchor_theorem": {
            "u2_is_the_unique_most_balanced_selector_family": (
                most_balanced_family == "U2"
                and balance_selectors["U2"] > balance_selectors["U1"] + TOL
                and balance_selectors["U2"] > balance_selectors["U3"] + TOL
            ),
            "u2_is_exactly_heavy_min_and_light_max": (
                heavy_descending[-1] == "U2" and light_descending[0] == "U2"
            ),
            "diffuse_quark_family_parity_singles_out_u2": (
                singled_family_label == "U2"
                and h1_family_sign == [-1, 1, -1]
                and hbar1_family_sign == [1, -1, 1]
            ),
            "best_legacy_block_candidate_commutes_with_the_same_family_parity": (
                float(np.linalg.norm(commutator)) < TOL
            ),
            "best_legacy_block_candidate_decouples_the_middle_family_exactly": (
                float(outer_middle_coupling) < TOL
                and abs(
                    float(
                        (middle_projector @ best_block_v @ middle_projector)[
                            singled_family_index, singled_family_index
                        ]
                    )
                    - 1.0
                )
                < TOL
            ),
            "best_vertex_level_quark_scan_anchors_both_sectors_on_block_u2": (
                int(best_vertex["v_up_block"]) == singled_family_index
                and int(best_vertex["v_dn_block"]) == singled_family_index
            ),
            "best_vertex_level_quark_scan_breaks_exact_diffuse_parity_but_keeps_the_same_anchor": (
                int(best_vertex["v_up_block"]) == singled_family_index
                and int(best_vertex["v_dn_block"]) == singled_family_index
                and float(np.linalg.norm(vertex_commutator)) > 1e-6
            ),
            "quark_side_reduces_to_middle_anchor_plus_outer_pair_shell": (
                most_balanced_family == "U2"
                and singled_family_label == "U2"
                and float(np.linalg.norm(commutator)) < TOL
                and float(outer_middle_coupling) < TOL
                and int(best_vertex["v_up_block"]) == singled_family_index
                and int(best_vertex["v_dn_block"]) == singled_family_index
            ),
        },
        "interpretive_read": (
            "Inference from independent exact repo data: the quark-bearing side "
            "already singles out one distinguished family. It is the unique "
            "least-split selector family U2, the unique positive entry in the "
            "diffuse Higgs family parity (-,+,-), the exact fixed family in the "
            "best legacy block CKM candidate, and the shared anchor block in "
            "the best vertex-level up/down scan."
        ),
        "bridge_verdict": (
            "The current quark-side architecture is no longer best read as a "
            "generic three-family cloud. The exact data reduce it to a middle-"
            "family anchor with an outer-pair mixing shell. U2 is the unique "
            "most balanced selector family, the diffuse Higgs packet singles "
            "out that same family with parity (-,+,-), the best exact legacy "
            "block candidate commutes with that parity and decouples the middle "
            "family, and the best vertex-level up/down scan anchors both "
            "sectors on block U2 while breaking exact parity."
        ),
        "source_files": [
            "data/w33_three_family_seesaw_bridge_summary.json",
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_middle_family_anchor_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
