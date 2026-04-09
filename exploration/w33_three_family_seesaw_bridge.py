"""Three-family seesaw structure inside the native selector ``3U`` packet.

This module sharpens the six-scale scaffold by organizing it into three exact
mixed-sign family blocks.

For each selector-side hyperbolic block U_i, the real symmetric 2x2 packet has
one positive and one negative eigenvalue. This defines a canonical pair

    heavy_i = lambda_i^+,
    light_i = -lambda_i^-,

with product heavy_i * light_i = -det(U_i).

So the current repo already contains three exact heavy/light family pairs.
Moreover, the heavy and light orderings are not the same across U1, U2, U3, so
the real selector packet is richer than any one-weight-per-family model.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_three_family_seesaw_bridge_summary.json"


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_three_family_seesaw_summary() -> dict[str, Any]:
    selector = _read_json("w33_selector_three_u_hierarchy_bridge_summary.json")
    blocks = selector["u_blocks"]

    pairs: dict[str, Any] = {}
    for name, block in blocks.items():
        eig = sorted(block["eigenvalues"])
        light = -eig[0]
        heavy = eig[1]
        pairs[name] = {
            "heavy_scale": heavy,
            "light_scale": light,
            "seesaw_ratio": heavy / light,
            "geometric_mean": (heavy * light) ** 0.5,
            "determinant_abs": abs(block["determinant"]),
        }

    heavy_order = sorted(pairs, key=lambda key: pairs[key]["heavy_scale"], reverse=True)
    light_order = sorted(pairs, key=lambda key: pairs[key]["light_scale"], reverse=True)
    ratio_order = sorted(pairs, key=lambda key: pairs[key]["seesaw_ratio"], reverse=True)

    return {
        "status": "ok",
        "family_pairs": pairs,
        "orderings": {
            "heavy_descending": heavy_order,
            "light_descending": light_order,
            "seesaw_ratio_descending": ratio_order,
        },
        "three_family_seesaw_theorem": {
            "each_u_block_defines_exact_heavy_light_pair": all(
                block["mixed_signature"] for block in blocks.values()
            ),
            "three_exact_family_pairs_exist": len(pairs) == 3,
            "each_pair_has_positive_heavy_light_product": all(
                pair["heavy_scale"] > 0.0 and pair["light_scale"] > 0.0 for pair in pairs.values()
            ),
            "heavy_light_product_matches_abs_determinant": all(
                abs(pair["heavy_scale"] * pair["light_scale"] - pair["determinant_abs"]) < 1e-12
                for pair in pairs.values()
            ),
            "heavy_and_light_orderings_are_not_the_same": heavy_order != light_order,
            "selector_packet_is_richer_than_one_weight_per_family_model": (
                heavy_order != light_order
            ),
        },
        "interpretive_read": (
            "Inference from the exact selector packet: the hyperbolic core does "
            "not merely supply six unrelated scales. It supplies three exact "
            "family seesaw pairs, and the mismatch between heavy and light "
            "orderings shows that a single scalar per family is already too small."
        ),
        "bridge_verdict": (
            "The native selector-side ``3U`` packet already contains a genuine "
            "three-family seesaw structure. Each U factor gives one heavy/light "
            "pair, but the family ordering of the heavy branch differs from the "
            "family ordering of the light branch. So the actual bridge packet is "
            "strictly richer than a single family weight model. The remaining "
            "physics problem is to decide which fermion sectors read off the "
            "heavy branch, which read off the light branch, and which couplings "
            "mix the two."
        ),
        "source_files": [
            "data/w33_selector_three_u_hierarchy_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_three_family_seesaw_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
