"""Parity-odd anchor bridge for the current quark mixing frontier.

The new middle-family anchor theorem showed that the quark-bearing side is
organized by the diffuse family parity ``P = diag(-1,+1,-1)`` and a shared
``U2`` anchor. The remaining exact question is what changes when we move from
the best parity-preserving block candidate to the better CKM-like vertex scan.

This module packages the minimal exact answer. Relative to the diffuse parity
operator, the current quark candidates split as

    V = V_even + V_odd,

where

- ``V_even = (V + P V P)/2`` preserves the middle-family anchor and the
  outer-pair shell;
- ``V_odd = (V - P V P)/2`` is supported only on outer<->middle channels.

For the best exact legacy block candidate, the odd bridge vanishes. For the
better CKM-like vertex scan, the odd bridge is nonzero of rank ``2`` and is
the entire parity-breaking correction. Both candidates remain real and have
vanishing Jarlskog invariant, so the next missing ingredient is CP phase, not
family placement.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_parity_odd_anchor_bridge_summary.json"
TOL = 1e-10


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _matrix_support_norms(matrix: np.ndarray) -> dict[str, float]:
    outer = [0, 2]
    middle = [1]
    return {
        "outer_outer_norm": float(np.linalg.norm(matrix[np.ix_(outer, outer)])),
        "middle_middle_norm": float(np.linalg.norm(matrix[np.ix_(middle, middle)])),
        "outer_to_middle_norm": float(np.linalg.norm(matrix[np.ix_(outer, middle)])),
        "middle_to_outer_norm": float(np.linalg.norm(matrix[np.ix_(middle, outer)])),
    }


def _decompose_against_parity(matrix: np.ndarray, parity: np.ndarray) -> dict[str, Any]:
    even = 0.5 * (matrix + parity @ matrix @ parity)
    odd = 0.5 * (matrix - parity @ matrix @ parity)
    return {
        "even": even,
        "odd": odd,
        "odd_rank": int(np.linalg.matrix_rank(odd, tol=TOL)),
        "odd_norm": float(np.linalg.norm(odd)),
        "commutator_norm": float(np.linalg.norm(matrix @ parity - parity @ matrix)),
        "even_support_norms": _matrix_support_norms(even),
        "odd_support_norms": _matrix_support_norms(odd),
    }


@lru_cache(maxsize=1)
def build_parity_odd_anchor_bridge_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    anchor = _load_json("w33_middle_family_anchor_bridge_summary.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(float)
    best_block_v = np.array(blocks["best_block"]["V_CKM"], dtype=float)
    best_vertex_v = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=float)

    best_block = _decompose_against_parity(best_block_v, parity)
    best_vertex = _decompose_against_parity(best_vertex_v, parity)

    return {
        "status": "ok",
        "diffuse_family_parity": [int(value) for value in signs["h1_family_sign_vector"]],
        "anchored_family_label": anchor["diffuse_quark_family_parity"]["singled_family_label"],
        "best_legacy_block_candidate": {
            "matrix": [[float(value) for value in row] for row in best_block_v.tolist()],
            "parity_even_part": [[float(value) for value in row] for row in best_block["even"].tolist()],
            "parity_odd_part": [[float(value) for value in row] for row in best_block["odd"].tolist()],
            "odd_rank": best_block["odd_rank"],
            "odd_norm": best_block["odd_norm"],
            "commutator_norm": best_block["commutator_norm"],
            "odd_support_norms": best_block["odd_support_norms"],
            "jarlskog": float(blocks["best_block"]["Jarlskog"]),
            "ckm_error": float(blocks["best_block"]["ckm_error"]),
        },
        "best_vertex_scan_candidate": {
            "matrix": [[float(value) for value in row] for row in best_vertex_v.tolist()],
            "parity_even_part": [[float(value) for value in row] for row in best_vertex["even"].tolist()],
            "parity_odd_part": [[float(value) for value in row] for row in best_vertex["odd"].tolist()],
            "odd_rank": best_vertex["odd_rank"],
            "odd_norm": best_vertex["odd_norm"],
            "commutator_norm": best_vertex["commutator_norm"],
            "odd_support_norms": best_vertex["odd_support_norms"],
            "jarlskog": float(blocks["vertex_scan_best"]["Jarlskog"]),
            "ckm_error": float(blocks["vertex_scan_best"]["ckm_error"]),
        },
        "parity_odd_anchor_bridge_theorem": {
            "best_exact_block_candidate_is_parity_even": (
                best_block["odd_norm"] < TOL and best_block["commutator_norm"] < TOL
            ),
            "best_exact_block_candidate_is_middle_anchor_plus_outer_pair_shell": (
                best_block["odd_norm"] < TOL
                and best_block["even_support_norms"]["outer_outer_norm"] > TOL
                and best_block["even_support_norms"]["middle_middle_norm"] > TOL
                and best_block["even_support_norms"]["outer_to_middle_norm"] < TOL
                and best_block["even_support_norms"]["middle_to_outer_norm"] < TOL
            ),
            "best_vertex_scan_is_even_shell_plus_nonzero_parity_odd_bridge": (
                best_vertex["odd_norm"] > 1e-6
                and best_vertex["odd_support_norms"]["outer_outer_norm"] < TOL
                and best_vertex["odd_support_norms"]["middle_middle_norm"] < TOL
                and best_vertex["odd_support_norms"]["outer_to_middle_norm"] > 1e-6
                and best_vertex["odd_support_norms"]["middle_to_outer_norm"] > 1e-6
            ),
            "best_vertex_scan_parity_odd_bridge_has_rank_two": best_vertex["odd_rank"] == 2,
            "parity_breaking_enters_only_through_anchor_to_outer_couplings": (
                best_vertex["odd_support_norms"]["outer_outer_norm"] < TOL
                and best_vertex["odd_support_norms"]["middle_middle_norm"] < TOL
                and best_vertex["odd_support_norms"]["outer_to_middle_norm"] > 1e-6
                and best_vertex["odd_support_norms"]["middle_to_outer_norm"] > 1e-6
            ),
            "both_current_quark_candidates_are_real_and_cp_silent": (
                abs(float(blocks["best_block"]["Jarlskog"])) < TOL
                and abs(float(blocks["vertex_scan_best"]["Jarlskog"])) < TOL
            ),
            "current_quark_frontier_is_anchor_bridge_not_cp_phase_solution": (
                best_vertex["odd_rank"] == 2
                and best_vertex["odd_support_norms"]["outer_outer_norm"] < TOL
                and best_vertex["odd_support_norms"]["middle_middle_norm"] < TOL
                and abs(float(blocks["best_block"]["Jarlskog"])) < TOL
                and abs(float(blocks["vertex_scan_best"]["Jarlskog"])) < TOL
            ),
        },
        "interpretive_read": (
            "Inference from the exact quark candidates: the move from the exact "
            "parity-preserving block model to the better CKM-like vertex scan is "
            "not a change of anchor family. It is the addition of a parity-odd "
            "rank-2 bridge coupling the anchored middle family to the outer pair."
        ),
        "bridge_verdict": (
            "The current quark mixing frontier has a minimal exact form. The best "
            "legacy candidate is purely parity-even and equals a middle anchor "
            "plus outer-pair shell. The better CKM-like candidate keeps the same "
            "anchor and adds a parity-odd rank-2 bridge supported only on "
            "middle-to-outer couplings. Both candidates remain real with "
            "vanishing Jarlskog invariant. So the remaining wall is not family "
            "assignment or mixing support. It is the origin of a complex CP "
            "phase on top of the anchored parity bridge."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_middle_family_anchor_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_parity_odd_anchor_bridge_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
