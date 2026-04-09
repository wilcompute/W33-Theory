"""Native six-scale hierarchy on the selector-side ``3U`` packet.

This module upgrades the abstract non-factorized ``3U`` block theorem by using
the actual repo-native selector packet on the three hyperbolic factors.

What is established here:
  - the selector-side reduced A4 packet splits across U1, U2, U3 as three real
    2x2 mixed-sign forms;
  - each U_i block is nonzero and not proportional to the pure hyperbolic form
        H = [[0,1],[1,0]];
  - the exact singular spectra of those three blocks are:

        U1: 0.50701374, 0.00105863
        U2: 0.08134017, 0.00375944
        U3: 2.47123616, 0.00045680

    so the combined 3U packet already carries six distinct positive scales.

So once the bridge is promoted from the primitive-plane toy model to the actual
selector-side ``3U`` packet, the family problem is no longer merely three
weights. The hyperbolic core already supports a native six-scale hierarchy.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

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

from w33_k3_selector_a4_five_factor_bridge import build_k3_selector_a4_five_factor_bridge_summary


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_selector_three_u_hierarchy_bridge_summary.json"
FLOAT_TOL = 1e-10
HYPERBOLIC_FORM = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)


def _spectral_packet(matrix: np.ndarray) -> dict[str, Any]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return {
        "determinant": float(np.linalg.det(matrix)),
        "eigenvalues": [float(value) for value in eigenvalues],
        "singular_values": [float(value) for value in singular_values],
    }


def _scalar_multiple_of_hyperbolic(matrix: np.ndarray) -> bool:
    if abs(matrix[0, 1]) < FLOAT_TOL and abs(matrix[1, 0]) < FLOAT_TOL:
        return np.allclose(matrix, 0.0, atol=FLOAT_TOL)
    mu = matrix[0, 1]
    return np.allclose(matrix, mu * HYPERBOLIC_FORM, atol=FLOAT_TOL)


@lru_cache(maxsize=1)
def build_selector_three_u_hierarchy_summary() -> dict[str, Any]:
    summary = build_k3_selector_a4_five_factor_bridge_summary()

    blocks = {
        "U1": np.array(summary["u_factor_one_packet_form"], dtype=float),
        "U2": np.array(summary["u_factor_two_packet_form"], dtype=float),
        "U3": np.array(summary["u_factor_three_packet_form"], dtype=float),
    }

    packets = {name: _spectral_packet(block) for name, block in blocks.items()}
    all_positive_singulars = sorted(
        [
            value
            for packet in packets.values()
            for value in packet["singular_values"]
            if value > FLOAT_TOL
        ],
        reverse=True,
    )

    return {
        "status": "ok",
        "u_blocks": {
            name: {
                "matrix": [[float(value) for value in row] for row in block.tolist()],
                **packets[name],
                "mixed_signature": (
                    packets[name]["eigenvalues"][0] < -FLOAT_TOL
                    and packets[name]["eigenvalues"][1] > FLOAT_TOL
                ),
                "scalar_multiple_of_hyperbolic_form": _scalar_multiple_of_hyperbolic(block),
            }
            for name, block in blocks.items()
        },
        "combined_three_u_positive_singular_scales": all_positive_singulars,
        "selector_three_u_hierarchy_theorem": {
            "all_three_u_blocks_are_nonzero": all(
                np.linalg.norm(block) > FLOAT_TOL for block in blocks.values()
            ),
            "all_three_u_blocks_are_mixed_signature": all(
                packets[name]["eigenvalues"][0] < -FLOAT_TOL
                and packets[name]["eigenvalues"][1] > FLOAT_TOL
                for name in blocks
            ),
            "no_u_block_is_just_scalar_times_hyperbolic_form": all(
                not _scalar_multiple_of_hyperbolic(block)
                for block in blocks.values()
            ),
            "combined_three_u_packet_has_six_distinct_positive_scales": (
                len(set(round(value, 12) for value in all_positive_singulars)) == 6
            ),
            "actual_selector_three_u_packet_evades_three_scalar_cartan_model": (
                all(
                    not _scalar_multiple_of_hyperbolic(block)
                    for block in blocks.values()
                )
                and len(set(round(value, 12) for value in all_positive_singulars)) == 6
            ),
        },
        "interpretive_read": (
            "Inference from the actual selector packet: the real ``3U`` bridge "
            "already contains more internal structure than the minimal scalar "
            "hyperbolic model. Each hyperbolic factor carries its own anisotropic "
            "mixed-sign block, and together they produce a native six-scale "
            "positive spectrum."
        ),
        "bridge_verdict": (
            "The actual selector-side ``3U`` packet breaks through the toy "
            "three-scalar model. Each U factor carries a genuine mixed-sign 2x2 "
            "block that is not just a scalar multiple of the hyperbolic form, "
            "and the combined positive singular spectrum contains six distinct "
            "scales. So the current repo already supports a native six-scale "
            "hierarchy on the hyperbolic core. The remaining question is not "
            "whether hierarchy can appear there. It is how those six scales map "
            "onto the physical family data."
        ),
        "source_files": [
            "exploration/w33_k3_selector_a4_five_factor_bridge.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_selector_three_u_hierarchy_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
