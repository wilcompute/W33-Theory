"""Shared sign-vector structure of the diffuse Higgs pair.

This module sharpens the rigid pattern inside H_1 and Hbar_1.

The exact support data show:
  - H_1 uses the second weak quark component Q_{i,2} and the first lepton
    doublet L_1;
  - Hbar_1 uses the first weak quark component Q_{i,1} and the second lepton
    doublet L_2;
  - the family-sign packet on the Q-side is the same up to an overall minus:
        H_1   : (-1, +1, -1)
        Hbar_1: (+1, -1, +1) = -(-1, +1, -1);
  - the color-sign packet on the u_c / d_c side is likewise the same up to
    an overall minus:
        H_1   : (+1, -1, -1)
        Hbar_1: (-1, +1, +1) = -(+1, -1, -1).

So the diffuse quark-bearing pair is not amorphous. It is one rigid signed
packet mirrored between up- and down-type channels.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from exploration.w33_fermionic_connes_sector import build_clean_higgs_geometry_summary


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_diffuse_higgs_sign_vector_bridge_summary.json"


def _extract_q_family_vector(entries: list[dict[str, object]]) -> list[int]:
    packet = {}
    for entry in entries:
        left = str(entry["left_slot"])
        right = str(entry["right_slot"])
        if left.startswith("Q_") and right in {"nu_c", "e_c"}:
            family = int(left.split("_")[1])
            packet[family] = int(entry["value"])
    return [packet[index] for index in (1, 2, 3)]


def _extract_color_vector(entries: list[dict[str, object]], prefix: str) -> list[int]:
    packet = {}
    for entry in entries:
        right = str(entry["right_slot"])
        if right.startswith(prefix):
            color = int(right.split("_")[-1])
            packet[color] = int(entry["value"])
    return [packet[index] for index in (1, 2, 3)]


@lru_cache(maxsize=1)
def build_diffuse_higgs_sign_vector_summary() -> dict[str, Any]:
    summary = build_clean_higgs_geometry_summary()
    h1 = summary["yukawa_support"]["H_1"]
    hbar1 = summary["yukawa_support"]["Hbar_1"]

    h1_q = _extract_q_family_vector(h1)
    hbar1_q = _extract_q_family_vector(hbar1)
    h1_color = _extract_color_vector(h1, "u_c")
    hbar1_color = _extract_color_vector(hbar1, "d_c")

    return {
        "status": "ok",
        "h1_family_sign_vector": h1_q,
        "hbar1_family_sign_vector": hbar1_q,
        "h1_color_sign_vector": h1_color,
        "hbar1_color_sign_vector": hbar1_color,
        "diffuse_sign_vector_theorem": {
            "h1_uses_second_weak_quark_component": all(
                str(entry["left_slot"]).startswith("Q_") and str(entry["left_slot"]).endswith("_2")
                for entry in h1 if str(entry["left_slot"]).startswith("Q_")
            ),
            "hbar1_uses_first_weak_quark_component": all(
                str(entry["left_slot"]).startswith("Q_") and str(entry["left_slot"]).endswith("_1")
                for entry in hbar1 if str(entry["left_slot"]).startswith("Q_")
            ),
            "h1_q_family_vector_is_minus_plus_minus": h1_q == [-1, 1, -1],
            "hbar1_q_family_vector_is_opposite": hbar1_q == [1, -1, 1],
            "h1_color_vector_is_plus_minus_minus": h1_color == [1, -1, -1],
            "hbar1_color_vector_is_opposite": hbar1_color == [-1, 1, 1],
            "q_side_vectors_match_up_to_global_sign": hbar1_q == [-value for value in h1_q],
            "color_side_vectors_match_up_to_global_sign": hbar1_color == [-value for value in h1_color],
            "diffuse_pair_is_one_mirrored_signed_packet": (
                h1_q == [-1, 1, -1]
                and hbar1_q == [1, -1, 1]
                and h1_color == [1, -1, -1]
                and hbar1_color == [-1, 1, 1]
            ),
        },
        "interpretive_read": (
            "Inference from the exact support signs: H_1 and Hbar_1 use one "
            "common signed family/color packet, mirrored between the up-type "
            "and down-type diffuse channels."
        ),
        "bridge_verdict": (
            "The diffuse quark-bearing Higgs pair is rigid at sign level. H_1 "
            "uses the second weak quark component with family vector (-,+,-) "
            "and color vector (+,-,-), while Hbar_1 uses the complementary "
            "first weak quark component with the opposite signs. So the diffuse "
            "pair is not a loose eight-entry cloud; it is one mirrored signed "
            "packet split across up- and down-type channels."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_diffuse_higgs_sign_vector_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
